from django.db import models
from owner.models import Product, CustomUser
# Create your models here.
class Cart(models.Model):
    product_name = models.ForeignKey(Product, related_name='cart_product', on_delete=models.DO_NOTHING)
    cart_of = models.ForeignKey(CustomUser, related_name='cart_customer', on_delete=models.DO_NOTHING)
    