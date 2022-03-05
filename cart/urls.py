from unicodedata import name
from django import views
from django.urls import path
from . import views
urlpatterns = [
    path('',views.cart_page,name='cart_page'),
    path('add_to_cart/<int:product_id>/',views.add_to_cart,name='add_to_cart'),
    path('dicrement_cart/<int:product_id>/',views.dicrement_cart,name='dicrement_cart'),
    path('remove_cart/<int:product_id>/',views.remove_cart,name='remove_cart'),
    path('checkout',views.checkout,name='checkout')
]