from django.shortcuts import render, redirect, get_object_or_404
from .cart import Cart
from bake_app.models import Product
from django.views.decorators.http import require_POST
from .forms import AddProductForm
# Create your views here.

@require_POST
def cart_add(request, product_id = None):
    cart = Cart(request)
    product = get_object_or_404(Product, id = product_id)
    form = AddProductForm(request.POST)
    
    if form.is_valid():
        cart_detail = form.cleaned_data
        cart.add(product = product, quantity = cart_detail['quantity'], update_quantity = cart_detail['update'])
        print('OK')
     
    return redirect('cart:cart_detail')

def cart_remove(request, product_id = None):
    cart = Cart(request)
    product = get_object_or_404(Product, id = product_id)
    cart.remove(product)

    return redirect('cart:cart_detail')

def cart_detail(request):
    cart = Cart(request)
    total = Cart(request).get_total()
    length = Cart(request).__len__()
    for item in cart:
        item['update_quantity_form'] = AddProductForm(initial={'quantity': item['quantity'],'update':True})
    return render(request, 'cart_detail.html', {'cart':cart, 'total': total, 'length': length})