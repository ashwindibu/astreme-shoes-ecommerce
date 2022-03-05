import datetime
from distutils.log import error
from multiprocessing import context
from django.shortcuts import redirect, render
from products.models import Order,mycart
from .forms import OrderForm
import razorpay
# Create your views here.


client = razorpay.Client(auth=("api_key", "api_secret"))

def place_order(request, total=0,quantity=0):
    current_user = request.user

    cart_items = mycart.objects.filter(user_id =current_user)
    cart_count = cart_items.count()
    if cart_count <= 0:
        return redirect('homepage')

    shipping = 50
    grand_total = 0
    for cart_item in cart_items:
        total += (cart_item.product_id.product_price * cart_item.quantity)
        quantity += cart_item.quantity
    grand_total = total + shipping
    print("Entered 1st Part")

    if request.method == 'POST':
        form = OrderForm(request.POST)
        print('Entered 2nd part')
        if form.is_valid():
            print('Entered 3rd part')
            data = Order()
            data.user = current_user
            data.first_name = form.cleaned_data['first_name']
            data.last_name = form.cleaned_data['last_name']
            data.email = form.cleaned_data['email']
            data.phone = form.cleaned_data['phone']
            data.address_line_1 = form.cleaned_data['address_line_1']
            data.country = form.cleaned_data['country']
            data.state = form.cleaned_data['state']
            data.city = form.cleaned_data['city']
            data.postal_code = form.cleaned_data['postal_code']
            data.order_note = form.cleaned_data['order_note']
            data.tax = shipping
            data.order_total = grand_total
            data.ip = request.META.get('REMOTE_ADDR')
            data.save()

            yr = int(datetime.date.today().strftime('%Y'))
            dt = int(datetime.date.today().strftime('%d'))
            mt = int(datetime.date.today().strftime('%m'))
            d = datetime.date(yr,mt,dt)
            current_date = d.strftime("%Y%m%d")
            order_number = current_date + str(data.id)
            data.order_number = order_number
            data.save()

            
            order = Order.objects.get(user=current_user,is_ordered=False,order_number=order_number)
            context = {
                'order':order,
                'shipping':shipping,
                'total':total,
                'grand_total':grand_total,
            }
            return render(request,'payments.html',context)
        else:
            print(form)
            return redirect('cart_page')
    else:
        return redirect('checkout')
        

def payments(request):
    return render(request,'payments.html')