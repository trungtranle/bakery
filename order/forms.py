from django import forms
from order.models import Order


class OrderFrom(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['id', 'first_name','last_name', 'email', 'phone', 'address', 'city',]

