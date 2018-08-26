"""bakery URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, re_path, include

from django.conf import settings
from django.conf.urls.static import static

from bake_app import views

import cart.urls

import order.views
urlpatterns = [
    path('admin/', admin.site.urls),
    re_path(r'^$', views.main, name = 'index'),    
    re_path(r'^detail/(\d+)$', views.detail, name = 'detail'),
    re_path(r'^cart/', include(cart.urls)),
    re_path(r'^order', order.views.create_order, name = 'order'),
    re_path(r'register', views.register, name = 'register'),
    re_path(r'login', views.user_login, name = 'login'),
    re_path(r'logout', views.user_logout, name = 'logout'),
    re_path(r'^chart$', views.chart, name = 'chart'),
    re_path(r'^rss$', views.read_rss, name = 'read_rss')
    
] + static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
