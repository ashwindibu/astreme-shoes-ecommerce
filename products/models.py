import datetime
from distutils.command.upload import upload
import os
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
    is_available = models.IntegerField(default=True)

class products(models.Model):
    product_name = models.CharField(max_length=100)
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