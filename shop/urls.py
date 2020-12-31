from django.urls import path
from .import views


app_name = 'shop'

urlpatterns =[
    path('', views.homepage, name = 'homepage'),
    path('register', views.userRegister, name = 'userRegister'),
    path('login', views.loginpage, name ='login'),
    path('dologin', views.dologin, name = 'dologin'),
    path('logout',views.logout_user, name = "logout" ),
    path('allproducts', views.allproduct, name = 'allproduct'),
    path('allcategory', views.allcategory, name = 'allcategory'),
    path('product/<slug:slug>', views.specific, name = "specific"),
    path('product_details/<int:id>/<slug:slug>', views.product_details, name = 'product_details'),
    path('search', views.search, name= 'search'),
]