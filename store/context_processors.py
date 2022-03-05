from itertools import count
from multiprocessing import context
from products.models import category, mycart

def header_menu(request):
    menu = category.objects.all()   
    return dict(catego=menu)