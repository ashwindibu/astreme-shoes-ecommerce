from unicodedata import name
from django.urls import path
from . import views
urlpatterns = [
    path('',views.home_page,name='homepage'),
    path('homepage',views.home_page),
    path('signin',views.signin,name='signin'),
    path('signup',views.signup,name='signup'),
    path('collection/<int:cat_id>/',views.menscollection,name='collection'),
    path('product_details/<int:pro_id>/',views.product_details,name='product_details'),
    path('userlogout',views.userlogout,name='userlogout'),
    # otp paths
    path('phone_verification',views.phone_verification),
    path('token_validation', views.token_validation),
    path('verified', views.verified),
    
]