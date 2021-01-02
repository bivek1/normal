from django.shortcuts import render
from owner.forms import UserRegistration, OrderCreateForm
from owner.models import Customer, Category, Sub_Category, Product, OrderItem, CustomUser, Order
from django.http import HttpResponse, HttpResponseRedirect
from .models import Cart
from django.contrib import messages
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

# Create your views here.

def dashboard(request):
    try:
        cart = Cart.objects.filter(cart_of = request.user)
    except:
        cart = None
    
    dist = {
        'cart':cart,
    }
    return render(request, 'customerpage.html', dist)



@login_required(redirect_field_name='addtocart')
def add_cart(request, product_id):
    cart = Cart()
    dist = {
        'cart':cart
    }
    product = Product.objects.get(id = product_id)
    cart.product_name = product
    cart.cart_of = request.user
    cart.save()
        
    # return render(request, 'cartlist.html',dist)
    return HttpResponseRedirect(reverse('customer:checkList'))

@login_required
def check_list(request):
    try:
        cart = Cart.objects.filter(cart_of = request.user)
    except:
        cart = None
    
    discount = 0 
    total_amount = 0
    
    for c in cart:
        total_amount += c.product_name.price
    dist = {
        'cart':cart,
        'discount': discount,
        'total_amount': total_amount + discount,
    }
    return render(request, 'checkout.html', dist)
   
def deleteCart(request, cart_id):
    cart = Cart.objects.get(id = cart_id)
    cart.delete()
    return HttpResponseRedirect('/')


def delivery(request):
    orderF = OrderCreateForm()
    cart = Cart.objects.filter(cart_of = request.user)
    dist = {
        'of': orderF,
        'cart':cart
    }
    if request.method == 'POST':
        orderF = OrderCreateForm(request.POST)
        if orderF.is_valid():
            orderF = OrderCreateForm(request.POST)
            cd = orderF.cleaned_data
            first_name = cd['first_name']
            last_name = cd['last_name']
            number = cd['number']
            address = cd['address']
            city = cd['city']
            order = Order(first_name = first_name, last_name=last_name, number = number, address = address, city = city, order_by = request.user)
            order.save()
            for item in cart:
                order_item = OrderItem(order = order, product = item.product_name, price = item.product_name.price)
                order_item.save()
            cart.delete()  
            return HttpResponseRedirect(reverse('customer:yourorder', kwargs={'id':request.user.id}))
        else:
            return render(request, 'orderpage.html', dist )
    else:
        return render(request, 'orderpage.html', dist )
  

        

def yourorder(request, id):
    customer = CustomUser.objects.get(id = id)
    order = Order.objects.filter(order_by=customer)
    try:
        cart = Cart.objects.filter(cart_of = request.user)
    except:
        cart = None
    
    dist = {
        'order':order,
        'cart':cart,
    }
    return render(request, 'yourorder.html',dist)

