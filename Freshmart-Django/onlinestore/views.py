from django.shortcuts import render, redirect, get_object_or_404
from .models import Products, Order, OrderItem, CompletedOrderItem, Profile, SellOnFreshMart, Review
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.contrib import messages
import requests
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from .forms import UserForm, UpdateProfileForm
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import  auth
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.db.models import Q
from django.db.models import F, Sum
from django.db import IntegrityError
from django.core import serializers
import json








def store(request):
    products = Products.objects.all()
    search_results = request.session.pop('search_results', None)

    if search_results:
        
        search_results = json.loads(search_results)

        

    if request.method == 'POST':
        product_id = request.POST.get('product_id')
        product = Products.objects.get(id=product_id)

        if product.inventory <= 0:
            return redirect('store')

        if request.user.is_authenticated:
            order, created = Order.objects.get_or_create(user=request.user)
            order_item, item_created = OrderItem.objects.get_or_create(order=order, product=product)
            order_item.quantity 
            order_item.save()
            
        return redirect('cart')
    

    return render(request, 'store.html', {'products': products, 'search_results': search_results})


def productdetail(request, pk):
    product = get_object_or_404(Products, id=pk)
    if request.method == 'POST':
        comment = request.POST.get('comment')

        create_review = Review.objects.create(user=request.user, product=product, comment= comment)
        create_review.save()

    user_reviews = Review.objects.filter(product=product).order_by('date_created')
        
    return render (request, 'productdetail.html', {'product': product, 'user_reviews': user_reviews})

def cart(request):
    order_items = {}
    error_messages = messages.get_messages(request)
    if request.user.is_authenticated:
        order_items = OrderItem.objects.filter(order__user=request.user)

    subtotal_list = []
    total = 0
    for order_item in order_items:
        subtotal = order_item.product.price * order_item.quantity
        subtotal_list.append(subtotal)
        total += subtotal
    return render(request, 'cart.html', {'order_items': order_items, 'subtotal_list': subtotal_list, 'total': total, 'error_messages': error_messages})






 
def delete_item(request, pk):
    if request.user.is_authenticated:
        order_item = OrderItem.objects.get(id=pk)
        order_item.delete()
    

    return redirect('cart')



def update_item(request, pk):
    update_quantity_message = None
    if request.user.is_authenticated:
        order_item = OrderItem.objects.get(id=pk)
        if request.method == 'POST':
            quantity = int(request.POST.get('quantity'))

            if quantity > order_item.product.inventory:
                update_quantity_message = 'The requested quantity exceeds the available inventory.'
                messages.error(request, update_quantity_message)
            else:
                order_item.quantity = quantity
                order_item.save()
            return redirect('cart')
    
        
    return redirect('cart')


def checkout(request):

    total=0
    item_total = 0
    completed_order_item = None
    if request.user.is_authenticated:
        order_items = OrderItem.objects.filter(order__user=request.user)
        item_quantity_list = [order_item.quantity for order_item in order_items]
        item_total = sum(item_quantity_list)

        subtotal_list = [order_item.product.price * order_item.quantity for order_item in order_items]
        total = sum(subtotal_list)
        cart_item_count = order_items.aggregate(total_quantity=Sum('quantity'))['total_quantity']
        
        
        all_out_of_stock = order_items.filter(product__inventory__lte=0).exists()
        
        
        if all_out_of_stock or cart_item_count == 0:
            messages.error(request, 'Products are out of stock. Please remove any out-of-stock products from your cart before proceeding to checkout..')
            return redirect('cart')


        subtotal_list = [order_item.product.price * order_item.quantity for order_item in order_items]
        total = sum(subtotal_list)

    if request.method == 'POST':
        
        
        if request.user.is_authenticated:
            reference = request.POST.get('reference')
            verify_url = f"https://api.paystack.co/transaction/verify/{reference}"
            headers = {
                "Authorization": f"Bearer {settings.PAYSTACK_SECRET_KEY}"
            }
            response = requests.get(verify_url, headers=headers)
            data = response.json()

            if data['status'] and data['data']['status'] == 'success':
                order_items.update(is_ordered=True)
                phone_number = request.POST.get('phone_number')
                address = request.POST.get('address')

                for order_item in order_items:
                    product = order_item.product
                    product.inventory -= order_item.quantity
                    product.save()

                order_items.update(phone_number=phone_number, address= address)

                for order_item in order_items:
                    completed_order_item = CompletedOrderItem.objects.create(
                        order=order_item.order,
                        product=order_item.product,
                        quantity=order_item.quantity,
                        phone_number=order_item.phone_number,
                        is_ordered=order_item.is_ordered,
                        address = order_item.address
                    )
                    completed_order_item.save()
                    
                return redirect('completedorder')
            else:
                messages.error(request, 'Verification failed')
                return redirect('checkout')
                

    return render(request, 'checkout.html', {'total': total, 'item_total': item_total, 'paystack_public_key': settings.PAYSTACK_PUBLIC_KEY})

@login_required(login_url='store')
def completed_orders(request):
    return render(request, 'completedorders.html')

def search(request):
    if request.method == 'GET':
        query = request.GET.get('q')

        if query:
            results = Products.objects.filter(Q(name__icontains=query))
            
            serialized_results = serializers.serialize('json', results)
            
            request.session['search_results'] = serialized_results

    return redirect('store')

        

        


# # # # # # # # # # # # # # # # # # # #SIGNUP/LOGIN# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 

def register(request):
    form = UserForm()
    if request.method == "POST":
        form = UserForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password1'])
            user.save()  
            messages.success(request, "You have registered successfully")
            return redirect('signin')
        else:
            messages.error(request, 'Registration failed. Password must contain at least 8 characters.')
            return redirect('register')
    else:
        context = {'form': form}

    return render(request, 'register.html', context)


def signin(request):
    if request.method == 'POST':
            form = AuthenticationForm(request, data=request.POST)
            if form.is_valid():
                username = form.cleaned_data.get('username')
                password = form.cleaned_data.get('password')
                user = authenticate(username=username, password=password)
                if user is not None:
                    login(request, user)
                    return redirect('store')
            else:
                messages.info(request, 'Invalid username or password.. Please try again.')
                return redirect('signin')
    form = AuthenticationForm()
    context = {'form':form}
    return render(request, 'signin.html', context)

@login_required(login_url='store')
def createprofile(request):

    
        error_message = None
        form = UpdateProfileForm()
        if request.method == 'POST':
            form = UpdateProfileForm(request.POST)
        if form.is_valid():
                try:
                    profile_form= form.save(commit=False)
                    profile_form.user= request.user
                    profile_form.save()
                    form = UpdateProfileForm()
                    return redirect('profile')
                except IntegrityError:
                    error_message = "A profile already exists for this user."
    
    
        return render(request, 'create_profile.html',{'form': form, 'error_message': error_message})

@login_required(login_url='store')
def profile(request):

    profile = Profile.objects.filter(user=request.user)
    order_history = CompletedOrderItem.objects.filter(order__user=request.user)
    
    
    
    return render(request, 'profile.html', {'profile': profile, 'order_history': order_history})




    



    


def about_us(request):
    return render (request, 'aboutus.html')

def contact(request):
    
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone_number = request.POST.get('phone_number')
        subject = request.POST.get('subject')
        message = request.POST.get('content')
        
        
        sell_on_fresh_mart = SellOnFreshMart.objects.create(
            name=name,
            email=email,
            phone_number = phone_number,
            subject=subject,
            message=message
        )
        sell_on_fresh_mart.save()
        messages.success(request, "We'll contact you as soon as possible")
        
        
        
    return render(request, 'contact.html')

    
def become_a_rider(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone_number = request.POST.get('phone_number')
        subject = request.POST.get('subject')
        message = request.POST.get('content')
        
        
        sell_on_fresh_mart = SellOnFreshMart.objects.create(
            name=name,
            email=email,
            phone_number = phone_number,
            subject=subject,
            message=message
        )
        sell_on_fresh_mart.save()
        messages.success(request, "We'll contact you as soon as possible")
    return render (request, 'becomearider.html')

def subscription(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        subscribe = SellOnFreshMart.objects.create(email=email)
        subscribe.save()
        return redirect('store')




def logout(request):
    auth.logout(request)
    return redirect('signin')