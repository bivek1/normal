from django.shortcuts import render
from .forms import AddCat, AddSubCat, AddProduct
from .models import Customer, Category, Sub_Category, Product,Order
from django.contrib import messages
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse

# Create your views here.
def ownerDashboard(request):
    order = Order.objects.filter(status = '')
    dist = {
        'order':order,
    }
    return render(request, 'adminpage.html', dist)


def add_category(request):
    form = AddCat(request.POST or None)
    dist = {
        'form': form,
    }
    if form.is_valid():
        form = AddCat(request.POST)
        try:
            savedata = form.save(commit = False)
            savedata.save()
        except:
            messages.error(request, 'It has been added already')
            return render(request, 'add_category.html', dist)
        messages.error(request, 'Sucessfully Added')
        return HttpResponseRedirect(reverse('shop:allcategory'))
    else:
        return render(request, 'add_category.html', dist)
    return render(request, 'add_category.html', dist)

def addsubcat(request):
    form = AddSubCat(request.POST or None)
    category = Category.objects.all().order_by('name')
    dist = {
        'form': form,
        'category': category,
    }
    if form.is_valid():
        form = AddSubCat(request.POST, request.FILES)
        try:
            savedata = form.save(commit = False)
            savedata.save()
        except:
            messages.error(request, 'Sub Category slug match. It has been added already')
            return render(request, 'add_sub_category.html', dist)
        messages.success(request, 'Sucessfully Added')
        # return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        return HttpResponseRedirect(request.path_info)
    else:
        return render(request, 'add_sub_category.html', dist)
    return render(request, 'add_sub_category.html', dist)

def product_add(request):
    form = AddProduct(request.POST, request.FILES or None)
    dist = {
        'form':form,
    }
    if form.is_valid():
        form.save()
        messages.success(request, "Sucessfully added Product")
        return HttpResponseRedirect(reverse('shop:allproduct'))
    return render(request, 'add_product.html', dist)

def adminOrder(request):
    order = Order.objects.filter(status = '')
    sent_order = Order.objects.filter(status = 'Sent')
    dist = {
        'order':order,
        'sent_order': sent_order,
    }
    if request.method == 'POST':
        return render(request, 'adminorder.html',dist)
    
    else:
        return render(request, 'adminorder.html',dist)
    
def sent_order(request, id):
    sent = Order.objects.get(id = id)
    sent.status = 'Sent'
    sent.save()
    return HttpResponseRedirect(reverse('owner:adminOrder'))

def userlist(request):
    Ulist = Customer.objects.all()
    
    return render(request, 'user.html', {'use':Ulist})
    