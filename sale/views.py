from tkinter import EXCEPTION
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from sign.models import Users, Goods,SellGoods
import hashlib
from django.conf import settings  
#商家主页
def admin(request):
    try:
        id = request.COOKIES.get("userid")
        user = Users.objects.get(id=id)
        goods = Goods.objects.filter(is_active=True, from_id=id)
        if user.isSeller:
            return render(request, 'sale/goods.html', locals())
        else:
            return render(request, 'market/recommend.html')
    except:

        return render(request, 'sign/sign_in.html')

#编辑商家地址信息
def edit(request):
    if request.method == 'GET':
        try:
            id = request.COOKIES.get("userid")
            user = Users.objects.get(id=id)
            if user.isSeller:
                return render(request, 'sale/edit.html',locals())
            else:
                return render(request, 'market/recommend.html')
        except:

            return render(request, 'sign/sign_in.html')
    if request.method == 'POST':
        id = request.COOKIES.get("userid")
        user = Users.objects.get(id=id)
        user.location = request.POST['location']
        return render(request, 'sale/admin.html',locals())

#全部上架的货物
def goods(request):
    try:
        id = request.COOKIES.get("userid")
        user = Users.objects.get(id=id)
        goods = Goods.objects.filter(is_active=True, from_id=id)
        return render(request, 'sale/goods.html', locals())

    except:

        return render(request, 'sign/sign_in.html')
 #全部订单详情
def all(request):
    try:
        id = request.COOKIES.get("userid")
        user = Users.objects.get(id=id)
       #下单没发货的订单
        goods1 = SellGoods.objects.filter(is_active = True,from_id=id, status = 1)
        #获得详细信息并保存在列表中
        detailgoods1 = []
        for good1 in goods1:
            detailgood1 = Goods.objects.get(id = good1.good_id)
            detailgood1.num = good1.good_num
            detailgood1.edit_time = good1.edit_time
            detailgood1.sellid = good1.id
            detailgoods1.append(detailgood1)

        #发货未签收的订单
        goods2 = SellGoods.objects.filter(is_active = True,from_id=id, status = 2)
        #获得详细信息并保存在列表中
        detailgoods2= []
        for good2 in goods2:
            detailgood2= Goods.objects.get(id = good2.good_id)
            detailgood2.num = good2.good_num
            detailgood2.edit_time = good2.edit_time
            detailgood2.sellid = good2.id
            detailgoods2.append(detailgood2)

        #已经签收的订单
        goods3 = SellGoods.objects.filter(is_active = True,from_id=id, status = 3)
        #获得详细信息并保存在列表中
        detailgoods3= []
        for good3 in goods3:
            detailgood3= Goods.objects.get(id = good3.good_id)
            detailgood3.num = good3.good_num
            detailgood3.edit_time = good3.edit_time
            detailgood3.sellid = good3.id
            detailgoods3.append(detailgood3)

        return render(request, 'sale/all.html',locals())
    except:

        return render(request, 'sign/sign_in.html') 



#############################################################
#更新货物详细
def updata(request, good_id):
    try:
        good = Goods.objects.get(id=good_id)
    except Exception as e:
        print('error ID!')
        return HttpResponse('error ID!')

    if request.method == 'GET':

        return render(request, 'sale/updata.html', locals())

    elif request.method == 'POST':

        price = request.POST['price']
        desc = request.POST['desc']
        good.price = price
        good.desc = desc
        good.save()
        return HttpResponseRedirect('/sale/goods',locals())

#下架货物
def delete(request, good_id):
    try:
        good = Goods.objects.get(id=good_id)
    except Exception as e:
        print('error ID!')
        return HttpResponse('error ID!')

    good.is_active = False
    good.save()
    return HttpResponseRedirect('/sale/goods')

#添加新的货物
def addgoods(request):
    if request.method == "GET":
        id = request.COOKIES.get("userid")
        user = Users.objects.get(id=id)
        goods = Goods.objects.filter(from_id=id)
        return render(request, 'sale/addgoods.html', locals())

    elif request.method == "POST":
        id = request.COOKIES.get("userid")
       
        img = request.FILES['img']
        print(img.name)
        path = settings.STATICFILES_ROOT
        print(type(path))
        print(path)
        path0 = path+"/product_images/"+img.name
        print(path0)
        with open(path0, 'wb') as f:                #将图片以二进制的形式写入
            for data in img.chunks():
                f.write(data)

        if "remember" in request.POST:
            tuijian = True
        else:
            tuijian = False

        Goods.objects.create(name=request.POST['name'],img= img.name, from_id=id, is_recommend=tuijian, kinds=request.POST['kinds'],
                             price=request.POST['price'], discribe=request.POST['desc'])
        return HttpResponseRedirect("/sale/goods/")

#对用户下单的货物进行发货
def send(request,good_id):
    try:
        good = SellGoods.objects.get(is_active = True,id=good_id)
    except Exception as e:
        print('error ID!')
        return HttpResponse('error ID!')
    good.status = 2
    good.save()
    return HttpResponseRedirect('/sale/all')



