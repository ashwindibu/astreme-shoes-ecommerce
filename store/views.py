import email
from django.http import HttpResponse
from django.shortcuts import render,redirect

from store.models import Account
from .forms import CreateUserForm
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages,auth

# Create your views here.
def home_page(request):
    return render(request,'index.html')

    
def signin(request):
        if request.method == 'POST':
            email = request.POST['email']
            password = request.POST['password']
            user = auth.authenticate(request,email=email,password=password)
            if user is not None:
                user_block = Account.objects.get(email=email)
                if user_block.is_active == 1:
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
            print('fffff')
            messages.error(request,'Something Wrong, Enter correct details')
            return redirect(signup)
    context = {'form':form}
    return render(request,'signup.html',context)


def menscollection(request):
    return render(request,'listing-grid-full.html')

