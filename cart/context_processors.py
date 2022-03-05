from products.models import mycart,cart
from .views import _cart_id

def counter(request):
    cart_count = 0
    if 'admin' in request.path:
        return{}
    else:
        try:
            cart_sess = cart.objects.filter(cart_id = _cart_id(request))
            if request.user.is_authenticated:
                cart_items = mycart.objects.all().filter(user_id = request.user)
            else:
                cart_items = mycart.objects.all().filter(cartid = cart_sess[:1])
            for cart_item in cart_items:
                cart_count += cart_item.quantity    
        except cart.DoesNotExist:
            cart_count = 0
    return dict(cart_count= cart_count)