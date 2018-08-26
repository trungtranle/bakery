from django.shortcuts import render
from order.models import OrderItem
from order.forms import OrderFrom
from cart.cart import Cart
from bake_app.models import UserProfileInfo
from django.core.mail import EmailMessage
from django.template.loader import get_template
from django.core.mail import send_mail
from django.template import context


# Create your views here.
def create_order(request):
    cart = Cart(request)
    form = OrderFrom()
    if request.method == "POST":
        form = OrderFrom(request.POST)
        if form.is_valid():
            order = form.save()
            for item in cart:
                OrderItem.objects.create(order=order, product = item['product'], price = item['price'], quantity = item['quantity'])
            
            #send email
            '''
            subject = "We've received your order"
            to = [order.email]
            from_email = 'trung.tranle1310@gmail.com'

            message = get_template('email_order_detail.html').render({'cart':cart, 'order':order})
            msg = EmailMessage(subject, message, to=to, from_email=from_email)
            msg.content_subtype = 'html'
            msg.send()
            print('SENT')
            '''
            #clear cart
            cart.clear()

            return render(request, 'created.html', {'order': order})
    else:
        if request.user.is_authenticated:            
            user_profile = UserProfileInfo.objects.get(user_id = request.user.id)
            form = OrderFrom(initial={
                'first_name' : request.user.first_name, 
                'last_name': request.user.last_name,
                'email' : request.user.email,
                'phone' :user_profile.phone,
                'address': user_profile.address,
                'city' : user_profile.city})
        
        else:
            form = OrderFrom()

    return render(request, 'create.html', {'form':form, 'cart':cart})
