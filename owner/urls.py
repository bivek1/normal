from django.urls import path
from .import views

app_name = 'owner'
 
urlpatterns = [
   path('admindashboard', views.ownerDashboard, name ='ownerDashboard'),
   path('add_category', views.add_category, name = 'add_category'),
   path('addsubcategory', views.addsubcat, name = 'add_sub_cat'),
   path('add_product', views.product_add, name = 'add_product'),
   path('adminOrder', views.adminOrder, name = 'adminOrder'),
   path('sent_order/<int:id>',views.sent_order, name = 'sent_order'),
   path('userlist', views.userlist, name = 'user_list'),
]
