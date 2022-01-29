from unicodedata import name
from django.urls import path
from . import views

urlpatterns = [
    path('',views.adminlogin),
    path('admin_home',views.admin_home,name='admin_home'),
    path('admin_user',views.admin_user),
    path('user_block',views.user_block),
    path('searched',views.searched,name='searched'),
    path('all_product',views.all_product),
    path('add_product',views.admin_add_product),
    path('product_delete',views.product_delete),
    path('product_edit',views.product_edit),
    path('product_update',views.product_update),
    path('category_man',views.category_man),
    path('cat_delete',views.cat_delete),
    path('cat_view',views.cat_view),
    path('add_category',views.add_category),
    
]