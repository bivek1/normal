from django.urls import path
from .import views


app_name = 'customer'

urlpatterns =[
   
    path('customerdashboard', views.dashboard, name ='dashboard'),
    path('addtocart/<int:product_id>/', views.add_cart, name = "addtocart"),
    path('cartlist', views.check_list, name = 'checkList'),
    path('deletecart/<int:cart_id>', views.deleteCart, name = 'deleteCart'),
    path('deliveryinfo', views.delivery, name ='delivery'),
    path('yourorder/<int:id>', views.yourorder, name = 'yourorder'),
]