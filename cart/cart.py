from django.conf import settings
from bake_app.models import Product

class Cart(object):
    def __init__(self, request):
        self.session = request.session
        cart = self.session.get(settings.CART_SESSION_ID)

        if not cart:
            cart = self.session[settings.CART_SESSION_ID] = {}

        self.cart = cart

    def save(self):
        self.session[settings.CART_SESSION_ID] = self.cart
        self.session.modified = True
    
    def add(self, product, quantity = 1, update_quantity = False):
        product_id = str(product.pk)
        if product_id not in self.cart:
            self.cart[product_id] = {'quantity': 0, 'price': str(product.price)}
        if update_quantity:
            self.cart[product_id]['quantity'] = quantity
        else:
            self.cart[product_id]['quantity'] += quantity
        self.save()

    def remove(self, product):
        product_id = str(product.pk)
        if product_id in self.cart:
            del self.cart[product_id]
            self.save()
    
    def __iter__(self):
        product_ids = self.cart.keys()
        products = Product.objects.filter(id__in = product_ids)
        for product in products:
            self.cart[str(product.pk)]['product'] = product
        
        for item in self.cart.values():
            item['total_price'] = int(item['price']) * item['quantity']
            yield item
        
    def __len__(self):
        return sum(int(item['quantity']) for item in self.cart.values())

    def get_total(self):
        return sum(int(item['price']) * int(item['quantity']) for item in self.cart.values())

    def clear(self):
        self.cart = {}
        self.save()