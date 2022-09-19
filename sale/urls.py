from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    #商家主页
    path('admin/',views.admin),
    #编辑商家地址信息
    path('edit/',views.edit),
    #全部上架的货物
    path('goods/',views.goods),
    #对用户下单的货物进行发货
    path('send/<int:good_id>',views.send),
    #全部订单详情
    path('all/',views.all),
    #添加新的货物
    path('addgoods/',views.addgoods),
    #更新货物详细
    path('updata/<int:good_id>',views.updata),
    #下架货物
    path('delete/<int:good_id>',views.delete),
    
]
