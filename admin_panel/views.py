import email
from itertools import product
from xml.parsers import expat
from django.http import HttpResponse
from django.shortcuts import render,redirect
from store.models import Account
from products.models import category,products
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages,auth
from django.views.decorators.cache import never_cache
from django.utils.datastructures import MultiValueDictKeyError
# Create your views here.

def adminlogin(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        print(email)
        admin_user = auth.authenticate(email = email, password = password)
        if admin_user is not None:
            print('is uder')
            admin_user_details = Account.objects.get(email=email)
            if admin_user_details.is_staff ==1:
                messages.error(request,'You entered successfully')
                login(request,admin_user)
                return redirect(admin_home)
            else:
                messages.error(request,'This Account is not Admin')
                return render(request,'adminlogin.html')
        else:
                messages.error(request,'Enter correct admin details..')
                return render(request,'adminlogin.html')
    return render(request,'adminlogin.html')
        

@login_required(login_url='adminlogin')
def admin_home(request):
    return render(request,'adminhome.html')
    
@login_required(login_url='adminlogin')
def admin_user(request):
    userdetails = Account.objects.filter(is_staff=0).all()
    return render(request,'adminuser.html',{ 'user' : userdetails})

def user_block(request):
        id = request.GET.get('id')
        user = Account.objects.get( id = id )
        if user.is_active == 0:
            Account.objects.filter(id=id).update(is_active = 1)
        else:
            Account.objects.filter(id=id).update(is_active = 0)
        return redirect(admin_user)
        
def searched(request):
    if request.method == 'POST':
        val = request.POST.get('searched')
        print(val)
        admin_details = Account.objects.filter(firstname__icontains = val)
        return render(request,'adminuser.html',{ 'user' : admin_details})

@login_required(login_url='adminlogin')  
def all_product(request):
    all_product = products.objects.all()
    return render(request,'allproduct.html',{'all_pro':all_product})

@login_required(login_url='adminlogin')
def admin_add_product(request):
    if request.method == 'POST':
        cat = request.POST.get('categor')
        print(cat)
        product = products()
        product.product_name = request.POST.get('p_name')
        product.product_price = request.POST.get('p_price')
        product.product_stock_s = request.POST.get('p_stock_s')
        product.product_stock_m = request.POST.get('p_stock_m')
        product.product_stock_l = request.POST.get('p_stock_l')
        product.category_id_id = request.POST.get('categor')
        product.product_description = request.POST.get('p_description')
        try:
            product.product_img_1 = request.FILES['image1']
            product.product_img_2 = request.FILES['image2']
            product.product_img_3 = request.FILES['image3']
            product.product_img_4 = request.FILES['image4']
            product.save()
        except MultiValueDictKeyError:
            messages.error(request,'Need 4 Images')
            return redirect(admin_add_product)

    catego = category.objects.all()
    return render(request,'addproduct.html',{'category':catego})

def product_delete(request):
    pro_id = request.GET.get('id')
    products.objects.filter(id = pro_id).delete()
    messages.success(request,'Deleted Successfully')
    return redirect(all_product)

@login_required(login_url='adminlogin')
def product_edit(request):
    id = request.GET.get('id')
    produc = products.objects.filter(id = id)
    if produc :
        catego = category.objects.all()
        return render(request,'editproduct.html',{'pro_id':produc,'category':catego})

def product_update(request):
    id = request.POST.get('id')
    product_name = request.POST.get('p_name')
    product_price = request.POST.get('p_price')
    product_stock_s = request.POST.get('p_stock_s')
    product_stock_m = request.POST.get('p_stock_m')
    product_stock_l = request.POST.get('p_stock_l')
    category_id_id = request.POST.get('categor')
    product_description = request.POST.get('p_description')
    try:
        product_img_1 = request.FILES['image1']
        product_img_2 = request.FILES['image2']
        product_img_3 = request.FILES['image3']
        product_img_4 = request.FILES['image4']
        check = products.objects.filter(id = id).exists()
        print(id)
        print("THIS IS OK")
        if check == True:
            print("INSIDE THIS IS OK")
            products.objects.filter(id=id).update(product_name=product_name,product_price=product_price,product_stock_s=product_stock_s,product_stock_m=product_stock_m,product_stock_l=product_stock_l,category_id_id=category_id_id,product_description=product_description,product_img_1=product_img_1,product_img_2=product_img_2,product_img_3=product_img_3,product_img_4=product_img_4)
            messages.success(request,'Updated Successfully')
            return redirect(all_product)
        return redirect(all_product)
    except MultiValueDictKeyError:
        messages.error(request,'Need 4 Images')
        return redirect(admin_add_product)

@login_required(login_url='adminlogin')
def category_man(request):
    catego = category.objects.all()
    return render(request,'category_man.html',{'cato':catego})

def cat_delete(request):
    id = request.GET.get('id')
    category.objects.filter(id=id).delete()
    return redirect(category_man)

@login_required(login_url='adminlogin')
def cat_view(request):
    cat_id = request.GET.get('id')
    mens = products.objects.filter(category_id=cat_id)
    return render(request,"allcategory.html",{'all_pro':mens})

@login_required(login_url='adminlogin')
def add_category(request):
    if request.method == 'POST':
        catego = category()
        catego.cat_name = request.POST['cat_name']
        catego.save()
        messages.success(request,'Category add successfully')
        return redirect(category_man)
    return render(request,'addcategory.html')
    
def adminlogout(request):
    logout(request)
    return redirect(adminlogin)