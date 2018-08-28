from django.shortcuts import render, redirect
from bake_app.models import Product
from cart import forms
from bake_app.forms import UserFrom, UserProfileInfoForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
import matplotlib
matplotlib.use('agg')
import matplotlib.pyplot as plt
from django.conf import settings
from order.models import OrderItem
import datetime
import xlsxwriter
import os
import feedparser
from django.conf import settings

# Create your views here.
def main(request):
    cakes = Product.objects.filter(category = 1)
    pie = Product.objects.filter(category = 3)
    dessert = Product.objects.filter(category = 2)
    drink = Product.objects.filter(category = 4)
    return render(
        request,
        'index.html',
        context = {
            "cakes":cakes,
            "pies":pie,
            "desserts":dessert,
            "drinks":drink,
        })
def detail(request, id = None):
    item = Product.objects.get(pk = id)
    form = forms.AddProductForm()
    return render(request,'detail.html',{'item': item, 'form':form}
    )
def test(request):
    return render(
        request,
        'blog-single.html'
        
    )


def register(request):
    registered = False

    if request.method == "POST":
        form_user = UserFrom(data= request.POST)
        form_profile = UserProfileInfoForm(data = request.POST)

        if form_user.is_valid() and form_profile.is_valid():
            if form_user.cleaned_data['password'] == form_user.cleaned_data['password_confirm']:
                user = form_user.save()
                user.set_password(user.password)
                user.save()

                profile = form_profile.save(commit=False)
                profile.user = user

                if "picture" in request.FILES:
                    profile.picture = request.FILES['picture']
                profile.save()
                registered = True
                user_in = authenticate(username = form_user.cleaned_data['username'], password = form_user.cleaned_data['password'])
                login(request, user_in)
                
            else:
                form_user.add_error('password_confirm', 'The passwords do not match')
            
    else:
        form_user = UserFrom()
        form_profile = UserProfileInfoForm()

    return render(request, 'register.html', {"form_user":form_user, "form_profile": form_profile, "registered" : registered})

def user_login(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(username = username, password = password)
        if user:
            if user.is_active:
                login(request, user)
                print('OK')
                return redirect('index')


        else:
            return render(request, 'login.html',{'result':'Invalid username and password'})
    else: 
        return render(request, 'login.html')

@login_required
def user_logout(request):
    logout(request)
    return redirect('index')

def test_email(request):
    return render(request, 'email_order_detail.html')

def chart(request):
    product_list = []
    product_count = []
    product_name = []
    for item in Product.objects.all():
        product_list.append(item.id)
        product_name.append(item.name)
        count = 0
        for order in OrderItem.objects.all():
            if order.product_id == item.id:
                count += order.quantity
        product_count.append(count)
    
    #Plot Chart
    chart = plt.figure()
    plt.bar(product_name, product_count)
    plt.title('Sale for each item \n' + datetime.datetime.now().strftime('%Y-%m-%d %H-%M-%S'))
    plt.xlabel('Item')
    plt.ylabel('Sales')
    plt.xticks(rotation=90)
    plt.tight_layout()
    chart.savefig(settings.STATIC_ROOT + '\chart.png', type = 'png')
    
    #Excel Export
    list_to_write = []
    header = ['id', 'name','sales']
    list_to_write.append(header)

    for i in range(len(product_list)):
        line = [product_list[i], product_name[i], product_count[i]]
        list_to_write.append(line)

    result = None
    if request.method == "POST":
        file_name = "bakery_data" + datetime.datetime.now().strftime('%Y-%m-%d %H-%M-%S') + ".xlsx"
        desktop = os.path.join(os.environ['USERPROFILE'], 'Desktop')
        address = desktop + "/" + file_name

        write_excel_file(address, list_to_write)

        result = 'File Exported at ' + address
    return render(request, 'chart.html', {'result': result})

def write_excel_file(address, list_ghi):
    workbook = xlsxwriter.Workbook(address)
    worksheet = workbook.add_worksheet()
    row = 0
    for item in list_ghi:
        i = 0 
        while i < len(item):
            worksheet.write(row, i, item[i])
            i += 1
        row += 1
    workbook.close()

def read_rss(request):
    feed = feedparser.parse("https://vnexpress.net/rss/tin-moi-nhat.rss")
    return render(request, 'readrss.html', {'feed':feed})