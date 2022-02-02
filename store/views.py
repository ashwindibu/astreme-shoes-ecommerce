import email
from itertools import product
import os
import random
from django.http import HttpResponse
from django.shortcuts import render,redirect

from store.models import Account
from .forms import CreateUserForm
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages,auth
from products.models import products
from django.contrib.auth.decorators import login_required
from gtts import gTTS
from playsound import playsound


# Create your views here.


    
def signin(request):
        if request.method == 'POST':
            u_email = request.POST['email']
            u_password = request.POST['password']
            user = auth.authenticate(request,email=u_email,password=u_password)
            if user is not None:
                user_block = Account.objects.get(email=u_email)
                if user_block.is_active == 1:
                    request.session['useremail'] = u_email
                    username= user_block.firstname
                    txt ="hello "+username+" welcome back to astreme shoes"
                    ob=gTTS(txt)
                    ob.save('welcome2.mp3')
                    playsound('welcome2.mp3')
                    os.remove('welcome2.mp3')

                    return redirect(home_page)
                else:
                    messages.error(request,'User is blocked')
            else:
                messages.error(request,'Invalid Username and Password')
                return render(request,'signin.html')
        return render(request,'signin.html')


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


def menscollection(request):
    
    return render(request,'shoe_gridcollection.html')

def home_page(request):
    product = products.objects.order_by('?')[:8]
    return render(request,'index.html',{'product':product})

def product_details(request):
    pro_id = request.GET.get("id")
    product = products.objects.filter(id = pro_id)
    return render(request,'productdetail.html',{ 'product': product })

def userlogout(request):
    # txt2 ="ദാ മൈരെ നിൽക് അവിഡെ"
    # ob=gTTS(txt2,lang='ml')
    # ob.save('welcome3.mp3')
    # playsound('welcome3.mp3')
    # os.remove('welcome3.mp3')
    logout(request)
    return redirect(signin)
