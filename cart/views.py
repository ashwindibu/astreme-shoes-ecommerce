
from itertools import product
from django.shortcuts import get_object_or_404, redirect, render
from products.models import products,cart,mycart
from django.contrib.auth.decorators import login_required

# Create your views here.
def _cart_id(request):
    cart_s = request.session.session_key
    if not cart_s:
        cart_s = request.session.create()
    return cart_s

def add_to_cart(request, product_id):
   
    product = products.objects.get(id = product_id) #get the product.
    print(product.product_name)
    try:
        cart_sess = cart.objects.get(cart_id = _cart_id(request)) #get the cart using the cart_id present in the session.
    except cart.DoesNotExist:
        cart_sess = cart.objects.create(cart_id = _cart_id(request))
        cart_sess.save()
    try:
        cart_item = mycart.objects.get(product_id = product, cartid = cart_sess)
        cart_item.quantity += 1 #cart itam quantity increment.
        cart_item.save()
    except mycart.DoesNotExist:
        cart_item = mycart.objects.create(
            product_id = product,
            cartid = cart_sess,
            quantity = 1,
            )
        cart_item.save() 
    return redirect('cart_page')

def dicrement_cart(request,product_id):
    cart_sess = cart.objects.get(cart_id = _cart_id(request))
    product = get_object_or_404(products,id = product_id)
    if request.user.is_authenticated:
        cart_item = mycart.objects.get(product_id = product,user_id=request.user)
    else:
        cart_sess = cart.objects.get(cart_id = _cart_id(request))
        cart_item = mycart.objects.get(product_id = product,cartid=cart_sess)
    if cart_item.quantity > 1:
        cart_item.quantity -= 1
        cart_item.save()
    else:
        cart_item.delete()
    return redirect('cart_page')

def remove_cart(request,product_id):
    product = get_object_or_404(products,id = product_id)
    if request.user.is_authenticated:
            cart_item = mycart.objects.get(product_id = product,user_id=request.user)
    else:
        cart_sess = cart.objects.get(cart_id = _cart_id(request))
        cart_item = mycart.objects.get(product_id = product,cartid= cart_sess)
    cart_item.delete()
    return redirect(cart_page)

def cart_page(request, total = 0,quantity = 0,cart_items =None):
    try:
        if request.user.is_authenticated:
            cart_items = mycart.objects.filter(user_id = request.user, is_active = True)
        else:
            cart_sess = cart.objects.get(cart_id = _cart_id(request))
            cart_items = mycart.objects.filter(cartid = cart_sess, is_active = True)
        for cart_item in cart_items:
            total += (cart_item.product_id.product_price * cart_item.quantity)
            quantity = cart_item.quantity
            print(cart_item)
        shipping = 50
        grand_total = shipping + total
    except :
        context = {
        'cart_i':cart_items,
        
        }
        return render(request,'cart.html',context)

    context = {
        'total':total,
        'quantity':quantity,
        'cart_i':cart_items,
        'shipping':shipping,
        'grand_total':grand_total, 
    }
    return render(request,'cart.html',context)
@login_required(login_url='signin')
def checkout(request, total = 0,quantity = 0,cart_items =None):
    try:
        if request.user.is_authenticated:
            cart_items = mycart.objects.filter(user_id = request.user, is_active = True)
        else:
            cart_sess = cart.objects.get(cart_id = _cart_id(request))
            cart_items = mycart.objects.filter(cartid = cart_sess, is_active = True)
        for cart_item in cart_items:
            total += (cart_item.product_id.product_price * cart_item.quantity)
            quantity = cart_item.quantity
            print(cart_item)
        shipping = 50
        grand_total = shipping + total
    except :
        context = {
        'cart_i':cart_items,
        
        }

    context = {
        'total':total,
        'quantity':quantity,
        'cart_i':cart_items,
        'shipping':shipping,
        'grand_total':grand_total, 
    }
    return render(request,'checkout.html',context)