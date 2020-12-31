from django.contrib import admin
from .models import Customer, Owner, Product, Category, Sub_Category,Order, OrderItem
# Register your models here.
# Register your models here.

admin.site.register(Customer)
admin.site.register(Owner)
admin.site.register(Product)
admin.site.register(Category)
admin.site.register(Sub_Category)

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    raw_id_fields = ['product']
    
@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'first_name', 'last_name', 'number', 'address',  'city', 'paid', 'status', 'created', 'updated']
    list_filter = ['paid', 'created', 'updated','status']
    inlines = [OrderItemInline]
