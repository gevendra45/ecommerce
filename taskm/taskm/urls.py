"""taskm URL Configuration

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
from django.urls import path, re_path
from taskupdate.views import (register, login, logout1, addproduct, getproduct, paginateproduct, order, orderhistory, searchproduct)
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('register/', register),
    path('login/', login),
    path('logout/', logout1),
    path('token/refresh/', TokenRefreshView.as_view()),#, name='token_refresh'),
    path('addproduct/', addproduct),
    path('getproduct/', getproduct),
    re_path(r'paginateproduct/$', paginateproduct),
    path('order/', order),
    path('orderhistory/', orderhistory),
    re_path(r'searchproduct/$', searchproduct),
]