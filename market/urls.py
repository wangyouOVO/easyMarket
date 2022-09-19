from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    #推荐页面
    path('recommend/', views.recommend_goods),
    #食物，衣服，电子产品
    path('food/', views.food),
    path('cloths/', views.cloths),
    path('eproduct/', views.eproduct),
    #产品详情页
    path('goodsdetail/<int:good_id>', views.goodsdetail),
    #添加货物到购物车
    path('addgoodstocart/<int:good_id>', views.addgoodstocart),
    #下单
    path('addgoodstolist/<int:good_id>', views.addgoodstolist),
    #去到商家主页
    path('gotomarket/<int:from_id>', views.gotomarket),
    #购物车详情页
    path('cart/', views.cart),
    #签收货物
    path('signfor/<int:good_id>', views.signfor),
    #下单购物车中的货物
    path('fromcarttolist/<int:good_id>', views.fromcarttolist),
    #删除购物车中的货物
    path('removefromcart/<int:good_id>', views.removefromcart),
    #添加评论
    path('addcomments/<int:good_id>', views.addcomments)
]
