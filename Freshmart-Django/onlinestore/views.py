from django.shortcuts import render, redirect, get_object_or_404
from .models import Products, Order
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.contrib import messages
import requests
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from .forms import UserForm
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import  auth
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.db.models import Q
from django.db.models import F, Sum



def store(request):
    products = Products.objects.all()

    if request.method == 'POST':
        product_id = request.POST.get('product_id')
        product = Products.objects.get(id=product_id)

        if product.inventory <= 0:
            messages.error(request, 'This product is currently out of stock.')
            return redirect('store')

        if request.user.is_authenticated:
            order, created = Order.objects.get_or_create(user=request.user, product=product)
        else:
            cart = request.session.get('cart', [])
            if product.id not in cart: 
                cart.append(product.id)
            print(cart)
            
            request.session['cart'] = cart
            
        return redirect('cart')
    

    return render(request, 'store.html', {'products': products})


def cart(request):
    if request.user.is_authenticated:
        order_items = Order.objects.filter(user=request.user)
    else:
        product_ids = request.session.get('cart', [])
        if isinstance(product_ids, int):
            product_ids = [product_ids]  
        products = Products.objects.filter(id__in=product_ids)
        
        order_items = []
        for product in products:
            quantity = product_ids.count(product.id)
            order_item = Order(product=product, quantity=quantity)
            order_items.append(order_item)

    subtotal_list = []
    total = 0

    for order_item in order_items:
        subtotal = order_item.product.price * order_item.quantity
        subtotal_list.append(subtotal)
        total += subtotal

    return render(request, 'cart.html', {'order_items': order_items, 'subtotal_list': subtotal_list, 'total': total})









 
def delete_item(request, pk):
    if request.user.is_authenticated:
        order_item = Order.objects.get(id=pk)
        order_item.delete()
    else:
        cart = request.session.get('cart', [])
        if pk in cart:
            cart.remove(pk)
            request.session['cart'] = cart

    return redirect('cart')



def update_item(request, pk):
    if request.user.is_authenticated:
        order_item = Order.objects.get(id=pk)
        if request.method == 'POST':
            quantity = int(request.POST.get('quantity'))

            if quantity > order_item.product.inventory:
                update_quantity_message = 'The requested quantity exceeds the available inventory.'
                messages.error(request, update_quantity_message)
            else:
                order_item.quantity = quantity
                order_item.save()
            return redirect('cart')
    else:
        product_id = pk
        cart = request.session.get('cart', [])
        
        if isinstance(cart, int):
            cart = []  
        
        for item in cart:
            if isinstance(item, dict) and item.get('product_id') == product_id:
                item['quantity'] = request.POST.get('quantity')
                request.session['cart'] = cart
                break
    context = {
        'update_quantity_message': update_quantity_message,  
    }
        
    return redirect('cart', context)


def checkout(request):
    if request.user.is_authenticated:
        order_items = Order.objects.filter(user=request.user)
        item_quantity_list = [order_item.quantity for order_item in order_items]
        item_total = sum(item_quantity_list)

        subtotal_list = [order_item.product.price * order_item.quantity for order_item in order_items]
        total = sum(subtotal_list)
        cart_item_count = order_items.aggregate(total_quantity=Sum('quantity'))['total_quantity']
        
        
        all_out_of_stock = order_items.filter(product__inventory__lte=0).exists()
        
        
        if all_out_of_stock or cart_item_count == 0:
            messages.error(request, 'All products are out of stock or your cart is empty. Please add products to your cart before checking out.')
            return redirect('cart')
    else:
        product_ids = request.session.get('cart', [])
        order_items = Order.objects.filter(product_id__in=product_ids)

        item_quantity_list = [order_item.quantity for order_item in order_items]
        item_total = sum(item_quantity_list)

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

                for order_item in order_items:
                    product = order_item.product
                    product.inventory -= order_item.quantity
                    product.save()

                order_items.update(phone_number=phone_number)
                return redirect('store')
            else:
                messages.error(request, 'Verification failed')
                return redirect('checkout')
        else:
            product_ids = request.session.get('cart', [])
            request.session['cart'] = list(product_ids)  
            return redirect('register')

    return render(request, 'checkout.html', {'total': total, 'item_total': item_total, 'paystack_public_key': settings.PAYSTACK_PUBLIC_KEY})





# # # # # # # # # # # # # # # # # # # #SIGNUP/LOGIN# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 

def register(request):
    form = UserForm()
    if request.method == "POST":
        form = UserForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password1'])
            user.save()
            product_ids = request.session.get('cart', [])
            order_items = Order.objects.filter(product_id__in=product_ids)
            User = get_user_model()  
            user_instance = User.objects.get(username=user.username)  
            for order_item in order_items:
                order_item.user_id = user_instance.id 
                order_item.save()

            request.session.pop('cart')  
            messages.success(request, "You have registered successfully")
            return redirect('signin')
        else:
            messages.error(request, 'Registration failed. Please check the form.')
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
                    return redirect('checkout')
            else:
                messages.info(request, 'Invalid username or password.. Please try again.')
                return redirect('signin')
    form = AuthenticationForm()
    context = {'form':form}
    return render(request, 'signin.html', context)


def logout(request):
    auth.logout(request)
    return redirect('signin')