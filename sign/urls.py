from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    #登陆
    path('', views.sign_in),
    #注册
    path('register/', views.sign_up),
    #退出登陆
    path('delete/', views.delete_sign),
]
