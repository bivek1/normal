from django.db import models
from django.contrib.auth.models import AbstractUser
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.template.defaultfilters import slugify
from django.urls import reverse
# Create your models here.

class CustomUser(AbstractUser):
    user_type_data = (('owner', "Owner"), ('customer', 'Customer'))
    user_type = models.CharField(default = 'owner', choices = user_type_data, max_length = 10)
    email = models.EmailField(unique = True)
    
class Owner(models.Model):
    id = models.AutoField(primary_key = 1)
    admin = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    address = models.CharField(max_length = 200)
    created_at = models.DateTimeField(auto_now_add= True)
    updated_at = models.DateTimeField(auto_now_add=True)
    objects = models.Manager()
    def __str__(self):
        return self.admin.username
    
class Customer(models.Model):
    id = models.AutoField(primary_key = True)
    admin = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    number = models.BigIntegerField(null=True)
    Temporary_address = models.CharField(max_length = 300)
    street = models.CharField(max_length = 200)
    profile_pic = models.ImageField(upload_to = "Customer_Profile", blank = True)
    gender = models.CharField(max_length = 100, choices = (
        ('Male', 'Male'),
        ('Female', 'Female')
    ))
    objects = models.Manager()
    def __str__(self):
        return self.admin.email
    
class Category(models.Model):
    name = models.CharField(max_length = 200, db_index = True) 
    slug = models.SlugField(max_length= 200, unique = True)
    objects = models.Manager()
    class Meta:
        ordering = ('name',)
        verbose_name = 'category'
        verbose_name_plural = 'categories'
        
    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        if not self.id:
            self.slug = slugify(self.name)
        super(Category, self).save(*args, **kwargs)
    
    def get_absolute_url(self):
        return reverse("shop:specific", args=[self.slug])
    
class Sub_Category(models.Model):
    sub_name = models.CharField(max_length = 200)
    slug = models.SlugField(max_length=200, unique = True)
    category = models.ForeignKey(Category, related_name='category_name', on_delete= models.PROTECT)
    objects = models.Manager()
    class Meta:
        ordering = ('sub_name',)
        verbose_name = 'sub_category'
        verbose_name_plural = 'sub_categories'
        
    def __str__(self):
        return self.sub_name
    
    def save(self, *args, **kwargs):
        if not self.id:
            self.slug = slugify(self.sub_name)
        super(Sub_Category, self).save(*args, **kwargs)
        
    # def get_absolute_url(self):
    #     return reverse("shop:product_list_by_sub_category", args=[self.slug])
    
class Product(models.Model):
    category = models.ForeignKey(Category, related_name= 'products', on_delete= models.PROTECT)
    sub_category = models.ForeignKey(Sub_Category, related_name='sub_category', on_delete=models.PROTECT, null = True)
    name = models.CharField(max_length = 200, db_index = True)
    slug = models.SlugField(max_length=200, db_index= True)
    image = models.ImageField(upload_to = 'products/%Y/%m/%d', blank = True)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits= 20, decimal_places = 2)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add= True)
    available = models.BooleanField(default= True)

    class Meta:
        ordering = ('name',)
        index_together = (('id', 'slug'),)
        
    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        if not self.id:
            self.slug = slugify(self.name)
        super(Product, self).save(*args, **kwargs)
    def get_absolute_url(self):
        return reverse("shop:product_detail", args=[self.id, self.slug])
    
class Order(models.Model):
    first_name = models.CharField(max_length=50, blank = True)
    last_name = models.CharField(max_length=50)
    order_by = models.ForeignKey(CustomUser, on_delete=models.DO_NOTHING)
    number = models.IntegerField()
    address = models.CharField(max_length=250)
    city = models.CharField(max_length=100)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    paid = models.BooleanField(default=False)
    status = models.CharField(max_length = 200, choices = (
        ('Sent', 'Sent'),
        ('Delivered', 'Delivered'),
        ('Cancelled', 'Cancelled'),
    ))
    class Meta():
        ordering = ('-created',)
    
    def __str__(self):
        return f'Order {self.id}'
  
    def get_total_cost(self):
        return sum(item.get_cost() for item in self.items.all())
class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, related_name='order_items', on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    
    def __str__(self):
        return str(self.id)
    
    def get_cost(self):
        return self.price 
    
    
@receiver(post_save, sender=CustomUser)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        if instance.user_type == 'owner':
            Owner.objects.create(admin = instance)
        if instance.user_type == 'customer':
            Customer.objects.create(admin = instance)

@receiver(post_save, sender=CustomUser)
def _post_save_receiver(sender, instance, **kwargs):
    if instance.user_type == 'owner':
        instance.owner.save()
    if instance.user_type == 'customer':
        instance.customer.save()

