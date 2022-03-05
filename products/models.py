import datetime
from distutils.command.upload import upload
import os
from platform import mac_ver
from xml.parsers.expat import model
from django.db import models
# Create your models here.
from email.policy import default
from tkinter import CASCADE
from django.db import models
from django.forms import CharField, FloatField, ImageField, IntegerField
from store.models import Account,Address

def filepath(request, filename):
    old_filename = filename
    timeNow = datetime.datetime.now().strftime('%Y%m%d%H:%M:%S')
    filename = "%s%s" % (timeNow, old_filename)
    return os.path.join('', filename)

class category(models.Model):
    cat_name = models.CharField(max_length=100)
    category_img = models.ImageField(upload_to="images/")
    is_available = models.IntegerField(default=True)

class products(models.Model):
    product_name = models.CharField(max_length=100,null=True)
    product_price = models.FloatField(default=False)
    product_description = models.CharField(max_length=1000)
    category_id = models.ForeignKey(category, default=True, on_delete=models.CASCADE)
    product_stock_s = models.IntegerField(default=False)
    product_stock_m = models.IntegerField(default=False)
    product_stock_l = models.IntegerField(default=False)
    product_img_1 = models.ImageField(upload_to="images/")
    product_img_2 = models.ImageField(upload_to="images/")
    product_img_3 = models.ImageField(upload_to="images/")
    product_img_4 = models.ImageField(upload_to="images/")

class cart(models.Model):
    cart_id = models.CharField(max_length=200,blank=True)
    date_added = models.DateField(auto_now_add=True)

class mycart(models.Model):
    product_id = models.ForeignKey(products,default=True,on_delete=models.CASCADE)
    user_id = models.ForeignKey(Account,on_delete=models.CASCADE,null=True)
    cartid   = models.ForeignKey(cart,on_delete=models.CASCADE)
    quantity = models.IntegerField()
    is_active = models.BooleanField(default = True)
    buy_now = models.BooleanField(default = False)
    def sub_total(self):
        return self.product_id.product_price * self.quantity

class Payment(models.Model):
    user = models.ForeignKey(Account,on_delete=models.CASCADE)
    payment_id = models.CharField(max_length=100)
    payment_method = models.CharField(max_length=100)
    amount_paid = models.CharField(max_length=100)
    status = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

class Order(models.Model):
    STATUS = (
        ('New','New'),
        ('Accepted','Accepted'),
        ('Completed','Completed'),
        ('Cancelled','Cancelled'),
        )

    user = models.ForeignKey(Account, on_delete=models.SET_NULL, null=True)
    payment = models.ForeignKey(Payment,on_delete=models.SET_NULL, blank=True, null=True)
    order_number = models.CharField(max_length=20)
    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=20)
    phone = models.CharField(max_length=15)
    email = models.EmailField(max_length=50)
    address_line_1 = models.CharField(max_length=200)
    country = models.CharField(max_length=20)
    state = models.CharField(max_length=20)
    city = models.CharField(max_length=20)
    postal_code = models.CharField(max_length=10)
    order_note = models.CharField(max_length=200, blank=True)
    order_total = models.FloatField()
    tax = models.FloatField()
    status = models.CharField(max_length=10, choices=STATUS, default='New')
    ip = models.CharField(max_length=20, blank=True)
    is_ordered = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class OrderProduct(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    payment = models.ForeignKey(Payment, on_delete=models.SET_NULL, blank=True, null=True)
    user = models.ForeignKey(Account, on_delete=models.CASCADE)
    product = models.ForeignKey(products, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    product_price = models.FloatField()
    is_ordered = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    