# -*- coding: utf-8 -*-
from django.contrib import admin
from django.urls import path,include

 
urlpatterns = [
    path('admin/', admin.site.urls),
    path('',include('baseapp.urls')),
    # path('rooms/',include('baseapp.urls')
    #means it will use the urls file in the baseapp folder
]
