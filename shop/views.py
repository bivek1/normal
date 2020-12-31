from django.shortcuts import render
from owner.forms import UserRegistration
from owner.models import Customer, Category, Sub_Category, Product, OrderItem, CustomUser, Order
from django.http import HttpResponse, HttpResponseRedirect
from com.models import Cart
from django.contrib import messages
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout
# Create your views here.

def homepage(request):
    try:
        cart = Cart.objects.filter(cart_of = request.user)
    except:
        cart = None
    fixed_product = Product.objects.order_by('-id')[:4]
    userId = request.user.id
    subCategory = Sub_Category.objects.all()
    category = Category.objects.all()
    product = Product.objects.all()
    
    
    dist = {
        'cat':category,
        'sub':subCategory,
        'cart':cart,
        'product': product,
        'fixed_product':fixed_product,
        'use':userId,
    }
    return render(request, 'index.html', dist)


def userRegister(request):
    try:
        cart = Cart.objects.filter(cart_of = request.user)
    except:
        cart = None
    form = UserRegistration(request.POST or None)
    
    if form.is_valid():
        foms = UserRegistration(request.POST)
        cd = form.cleaned_data
        email = cd['email']
        password = cd['password']
        first_name = cd['first_name']
        last_name = cd['last_name']
        vend = CustomUser.objects.create_user(first_name = first_name, last_name = last_name, email = email, password = password, username = email, user_type = 'customer')

        messages.success(request, 'User Created Sucessfully. Please Login')
        return HttpResponseRedirect(reverse('shop:login'))
    else:
        return render(request, 'userregister.html', {'form': form, 'cart':cart})
            
    return render(request, 'userregister.html', {'form': form})
    
def loginpage(request):
    try:
        cart = Cart.objects.filter(cart_of = request.user)
    except:
        cart = None
    return render(request, 'login.html', {'cart':cart})

def dologin(request):
    if request.method == 'POST':
        username = request.POST['email']
        password = request.POST['password']
        
        user = authenticate(request, username =  username, password = password)
        if user != None:
            login(request, user)
            if user.user_type == "owner":
                return HttpResponseRedirect(reverse('owner:ownerDashboard'))
            if user.user_type == "customer":
                return HttpResponseRedirect(reverse('customer:dashboard'))
        else:
            messages.success(request, 'Invalid Credential')
            return HttpResponseRedirect(reverse('shop:login'))
    else:
        return HttpResponse("<H2>You Are now not Login</H2>")
    


def product_details(request, id, slug):
    p = Product.objects.get(id = id)
    try:
        cart = Cart.objects.filter(cart_of = request.user)
    except:
        cart = None
    dist = {
        'product': p,
        'cart':cart,
    }
    
    return render(request, 'product_details.html', dist)
    
    
def search(request):
    ans = request.GET['search']
    product = Product.objects.filter(name__icontains = ans)
    try:
        cart = Cart.objects.filter(cart_of = request.user)
    except:
        cart = None
    dist = {
        'ans':ans,
        'cart':cart,
        'product': product,
    }
    return render(request, 'search_result.html',dist)


def allcategory(request):
    try:
        cart = Cart.objects.filter(cart_of = request.user)
    except:
        cart = None
    category = Category.objects.all()
    return render(request, 'allcategory.html', {'category':category, 'cart':cart,})

def specific(request, slug):
    p = Category.objects.get(slug= slug)
    product = Product.objects.filter(category = p)
    try:
        cart = Cart.objects.filter(cart_of = request.user)
    except:
        cart = None
    return render(request, 'specific.html', {'product':product, 'cart':cart,'slug':slug})

def logout_user(request):
    logout(request)
    return HttpResponseRedirect('/')

def allproduct(request):
    products = Product.objects.filter(available=True)
    try:
        cart = Cart.objects.filter(cart_of = request.user)
    except:
        cart = None
    dist = {
        'product' : products,
        'cart':cart,
    }
    return render(request, 'allproduct.html', dist)