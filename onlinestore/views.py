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



def store(request):
    products = Products.objects.all()

    if request.method == 'POST':
        product_id = request.POST.get('product_id')
        product = Products.objects.get(id=product_id)

        if request.user.is_authenticated:
            order, created = Order.objects.get_or_create(user=request.user, product=product)
        else:
            cart = request.session.get('cart', [])
            cart.append(product.id)
            request.session['cart'] = cart
            print(request.session.get('cart'))


        return redirect('cart')

    return render(request, 'store.html', {'products': products})


def cart(request):
    if request.user.is_authenticated:
        order_items = Order.objects.filter(user=request.user)
        
    else:
        product_ids = request.session.get('cart', [])
        order_items = Order.objects.filter(product_id__in=product_ids)
        print(order_items)

    subtotal_list = [order_item.product.price * order_item.quantity for order_item in order_items]
    total = sum(subtotal_list)

    return render(request, 'cart.html', {'order_items': order_items, 'subtotal_list': subtotal_list, 'total': total})







def delete_item(request, pk):
    if request.user.is_authenticated:
        order_item = Order.objects.get(id=pk)
        order_item.delete()
    else:
        cart = request.session.get('cart', [])
        product_ids = [item['product_id'] for item in cart]

        if pk in product_ids:
            index = product_ids.index(pk)
            cart.pop(index)
            request.session['cart'] = cart

    return redirect('cart')




def update_item(request, pk):
    order_item = Order.objects.get(id=pk)

    if request.method == 'POST':
        quantity = request.POST.get('quantity')

        order_item.quantity = quantity

        order_item.save()
        return redirect('cart')




def checkout(request):
    if request.user.is_authenticated:
        order_items = Order.objects.filter(user=request.user)
        item_quantity_list = [order_item.quantity for order_item in order_items]
        item_total = sum(item_quantity_list)

        subtotal_list = [order_item.product.price * order_item.quantity for order_item in order_items]
        total = sum(subtotal_list)
    else:
        product_ids = request.session.get('cart', [])
        order_items = Order.objects.filter(product_id__in=product_ids)

        item_quantity_list = [order_item.quantity for order_item in order_items]
        item_total = sum(item_quantity_list)

        subtotal_list = [order_item.product.price * order_item.quantity for order_item in order_items]
        total = sum(subtotal_list)

    if request.method == 'POST':
        if request.user.is_authenticated:
            # Process checkout for authenticated user
            reference = request.POST.get('reference')
            verify_url = f"https://api.paystack.co/transaction/verify/{reference}"
            headers = {
                "Authorization": f"Bearer {settings.PAYSTACK_SECRET_KEY}"
            }
            response = requests.get(verify_url, headers=headers)
            data = response.json()

            if data['status'] and data['data']['status'] == 'success':
                # Payment is successful, update order status and perform other actions
                order_items.update(is_ordered=True)
                # Additional logic here to update other models or perform any necessary actions

                # Redirect to a success page or perform any other action
                return redirect('store')
            else:
                # Payment verification failed, handle the error appropriately
                # For example, you can display an error message or redirect to a failure page
                messages.error(request, 'Verification failed')
                return redirect('checkout')
        else:
            # Store order items in session and redirect to registration page
            product_ids = request.session.get('cart', [])
            request.session['cart'] = list(product_ids)  # Convert to a list of product IDs
            return redirect('register')

    return render(request, 'checkout.html', {'total': total, 'item_total': item_total, 'paystack_public_key': settings.PAYSTACK_PUBLIC_KEY})




# ...

from django.contrib.auth import get_user_model

# ...

def register(request):
    form_name = UserForm()
    if request.method == "POST":
        form = UserForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()

            # Retrieve cart items from session and associate them with the registered user
            product_ids = request.session.get('cart', [])
            order_items = Order.objects.filter(product_id__in=product_ids)
            User = get_user_model()  # Get the User model dynamically
            user_instance = User.objects.get(username=user.username)  # Fetch the User instance
            for order_item in order_items:
                order_item.user_id = user_instance.id  # Assign the user ID of the authenticated user
                order_item.save()

            request.session.pop('cart')  # Remove cart items from session
            messages.success(request, "You have registered successfully")
            return redirect('signin')
        else:
            messages.error(request, 'Registration failed. Please check the form.')
            return redirect('register')
    else:
        context = {'form': form}

    return render(request, 'register.html', context)






from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

def register(request):
    form = UserCreationForm()
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.password = make_password(form.cleaned_data['password1'])  # Securely set the password
            user.save()
            
            # Retrieve cart items from session and associate them with the registered user
            product_ids = request.session.get('cart', [])
            order_items = Order.objects.filter(product_id__in=product_ids)
            for order_item in order_items:
                order_item.user = user
                order_item.save()
            
            request.session.pop('cart')  # Remove cart items from session
            messages.success(request, "You have registered successfully")
            return redirect('signin')
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