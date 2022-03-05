
from turtle import home
from django.http import HttpResponse
from django.shortcuts import render,redirect

from store.models import Account
from .forms import CreateUserForm
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages,auth
from products.models import mycart,cart,products,category
from cart.views import _cart_id
from . import twilio_client
import os
from gtts import gTTS
from playsound import playsound
from django.core.paginator import EmptyPage,PageNotAnInteger,Paginator
import requests


# Create your views here.


    
def signin(request):
    if request.session.has_key('useremail'):
        return redirect(home_page)
    else:
        if request.method == 'POST':
            u_email = request.POST['email']
            u_password = request.POST['password']
            user = auth.authenticate(request,email=u_email,password=u_password)
            if user is not None:
                user_block = Account.objects.get(email=u_email)
                if user_block.is_active == 1:
                    try:
                        carts = cart.objects.get(cart_id = _cart_id(request))
                        is_cart_item_exists = mycart.objects.filter(cartid = carts).exists()
                        if is_cart_item_exists:
                            cart_item = mycart.objects.filter(cartid = carts)
                            for item in cart_item:
                                item.user_id = user
                                item.save()
                    except:
                        pass
                    request.session['useremail'] = u_email
                    auth.login(request,user)
                    print(user)
                    url = request.META.get('HTTP_REFERER')
                    try:
                        query = requests.utils.urlparse(url).query
                        print(query)
                        params = dict(x.split('=') for x in query.split('&'))
                        if 'next' in params: 
                            nextPage = params['next']
                            return redirect(nextPage)
                    except:
                        return redirect(home_page)
                else:
                    messages.error(request,'User is blocked')
            else:
                messages.error(request,'Invalid Username and Password')
                return render(request,'account/login.html')
        return render(request,'account/login.html')


def signup(request):
    form = CreateUserForm()
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            firstname = form.cleaned_data.get('firstname')
            messages.success(request, firstname +' Account created successfully ')
            return redirect(signin) 
        else:
            messages.error(request,'Something Wrong, Enter correct details')
            return redirect(signup)
    context = {'form':form}
    return render(request,'signup.html',context)


def menscollection(request,cat_id):
    # cat_id = request.GET.get('id')
    produc = products.objects.filter(category_id=cat_id).all()
    paginator = Paginator(produc,3)
    page = request.GET.get('page')
    paged_product = paginator.get_page(page)
    return render(request,'shoe_gridcollection.html',{'produc':paged_product})

def home_page(request):
    catego = category.objects.all()[:3]
    product = products.objects.order_by('?')[:8]
    if request.session.has_key('useremail'):
        user_sess = request.session['useremail']
        user = Account.objects.get(email=user_sess)
        user_name = user.firstname
        return render(request,'index.html',{'product':product,'catego':catego,'user_name':user_name})
    return render(request,'index.html',{'product':product,'catego':catego})

def product_details(request,pro_id):
    # pro_id = request.GET.get("id")
    product = products.objects.get(id = pro_id)
    in_cart = mycart.objects.filter(cartid__cart_id = _cart_id(request), product_id = product).exists()
    return render(request,'productdetail.html',{'product': product,'in_cart':in_cart})

def userlogout(request):
    logout(request)
    return redirect(home_page)




# OTP SYSTEMS

def phone_verification(request):
    if request.method == 'POST':
        phonenum = request.POST.get('phone')
        if phonenum:
            user_valid = Account.objects.filter(phone = phonenum)
            if user_valid:
                phone = '+91'+request.POST.get('phone')
                request.session['phone_number'] = phonenum
                twilio_client.verifications(phone, 'sms')
                print(phone)
                return redirect(token_validation)
            else:
                messages.success(request,'Invalid phone number')
                return render(request, 'phonelogin.html')
        else:
            return render(request, 'phonelogin.html')
    else:
        return render(request, 'phonelogin.html')


def token_validation(request):
    print("woek")

    if request.method == 'POST':
        verification = twilio_client.verification_checks('+91'+request.session['phone_number'], request.POST.get('otp'))
        if verification is None:
            messages.success(request,'Invalid OTP')
            return redirect(phone_verification)
        elif verification.status == 'approved':
            request.session['is_verified'] = True
            return redirect(verified)
        else:
            messages.success(request,'Invalid OTP')
            return redirect(token_validation)
    else:
        phone_num = request.session['phone_number']
        messages.success(request,phone_num)
        return render(request, 'phoneverification.html')


def verified(request):
    if not request.session.get('is_verified'):
        return redirect(phone_verification)
    phone = request.session['phone_number']   
    user = Account.objects.get(phone=phone) 
    request.session['useremail'] = user.email
    return redirect(signin)
