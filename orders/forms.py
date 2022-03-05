from django import forms
from  products.models import Order

class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['first_name','last_name','phone','email','address_line_1','country','state','city','postal_code','order_note']