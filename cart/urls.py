from django.contrib import admin
from django.urls import path, re_path, include
from cart import views

app_name = 'cart'
urlpatterns = [
    re_path(r'^cart_add/(\d+)/$', views.cart_add, name = 'cart_add'),
    re_path(r'^cart_remove/(\d+)/$', views.cart_remove, name = 'cart_remove'),
    re_path(r'^cart_detail/$', views.cart_detail, name = 'cart_detail'),
]