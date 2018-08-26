from django.db import models
from bake_app.models import Product
# Create your models here.

class Order(models.Model):
    first_name = models.CharField(max_length =100)
    last_name = models.CharField(max_length =100)
    email = models.EmailField()
    phone = models.CharField(max_length = 20)
    address = models.CharField(max_length = 200)
    city = models.CharField(max_length = 100)
    created = models.DateTimeField(auto_now=True)
    updated = models.DateTimeField(auto_now=True)
    paid = models.BooleanField(default = False)

    class Meta:
        ordering = ('-created',)

    def __str__(self):
        return 'Order {}'.format(self.id)

    def get_total_cost(self):
        return sum(item.get_cost() for item in self.items.all())

class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete = models.PROTECT)
    product = models.ForeignKey(Product, related_name='items', on_delete=models.PROTECT)
    price = models.IntegerField()
    quantity = models.PositiveIntegerField(default = 1)

    def __str__(self):
        return str(self.id)

    def get_cost(self):
        return self.price * self.quantity