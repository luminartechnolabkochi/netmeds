from django.db import models
from django.contrib.auth.models import User
from datetime import datetime, timedelta
class Customer(models.Model):
    name = models.CharField(max_length=200, null=True)
    phone = models.CharField(max_length=200, null=True)
    email = models.EmailField(max_length=200, null=True)
    date_created = models.DateTimeField(auto_now_add=True, null=True)
    address = models.CharField(max_length=200, null=True)
    password = models.CharField(max_length=200, null=True)
    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=200, null=True)
    cost = models.FloatField(null=True)
    vendor = models.CharField(max_length=200, null=True)
    discount = models.IntegerField(default=0)
    date_created = models.DateTimeField(auto_now_add=True, null=True)
    product_image= models.ImageField(upload_to="images")
    description=models.CharField(max_length=200,null=True)#sa
    category=models.CharField(max_length=200,null=True)

    def __str__(self):
        return self.name

class Cart(models.Model):
    options=(
        
        ('CANCELED','CANCELED'),
        ('ORDER-PLACED','ORDER-PLACED'),
        ('IN-CART','IN-CART'),
    
    )
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    product=models.ForeignKey(Product,on_delete=models.CASCADE)
    created_date=models.DateField(auto_now_add=True)
    status = models.CharField(max_length=200, null=True, choices=options,default="IN-CART")



class Order(models.Model):
    customer = models.ForeignKey(User, null=True, on_delete= models.CASCADE)
    product = models.ForeignKey(Product, null=True, on_delete= models.CASCADE)
    date_created = models.DateTimeField(auto_now_add=True, null=True)
    status = models.CharField(max_length=200, null=True, choices=(
        ('CANCELED','CANCELED'),
        ('COMPLETED','COMPLETED'),
        ('REFUNDED','REFUNDED'),
        ('PENDING PAYMENT','PENDING PAYMENT'),
        ("ORDER-PLACED","ORDER-PLACED"),
        ("IN-TRANSIT","IN-TRANSIT"),
        ("DELIVERED","DELIVERED")

    ),default="ORDER-PLACED")
    delivery_address=models.CharField(max_length=250,null=True)
    edate=datetime.now() + timedelta(days=5)
    delivery_date=models.DateField(default=edate)