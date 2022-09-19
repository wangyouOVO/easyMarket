from tkinter import EXCEPTION
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from grpc import Status
from sign.models import Users ,Goods ,SellGoods,Comment
import hashlib

#获得所有推荐的商品并输出给用户
def recommend_goods(request):
    try:
        id = request.COOKIES.get("userid")
        user = Users.objects.get(id=id)
        goods = Goods.objects.filter(is_active=True, is_recommend = True)
        if user.isSeller:
            return render(request, 'sign/sign_in.html')
        else:
            return render(request, 'market/recommend.html',locals())
    except:

        return render(request, 'sign/sign_in.html')   

#进入产品详情页，并且可以下单和添加到购物车
def goodsdetail(request,good_id):
        try:
            good = Goods.objects.get(is_active = True,id=good_id)
        except Exception as e:
            print('error ID!')
            return HttpResponse('error ID!')
        comments = Comment.objects.filter(is_active = True,good_id=good_id)
        detailcomments = []
        for comment in comments:
            user = Users.objects.get(id = comment.to_id)
            comment.fromname = user.name
            detailcomments.append(comment)
        return render(request, 'market/goodsdetail.html', locals())

#添加到购物车
def addgoodstocart(request,good_id):
        try:
            good = Goods.objects.get(is_active = True,id=good_id)
        except Exception as e:
            print('error ID!')
            return HttpResponse('error ID!')
        
        id = request.COOKIES.get("userid")
        SellGoods.objects.create(from_id=good.from_id, good_id=good_id, to_id=id, status=0)
        return HttpResponseRedirect("/market/goodsdetail/"+str(good_id))



#正式下单
def addgoodstolist(request,good_id):
        try:
            good = Goods.objects.get(is_active = True,id=good_id)
        except Exception as e:
            print('error ID!')
            return HttpResponse('error ID!')
        
        id = request.COOKIES.get("userid")
        SellGoods.objects.create(from_id=good.from_id, good_id=good_id, to_id=id, status=1, good_num=request.POST['sellgoodsnum'])
        return HttpResponseRedirect("/market/goodsdetail/"+str(good_id))

#进入商家店铺
def gotomarket(request,from_id):
        try:
            user = Users.objects.get(is_active = True,id = from_id)
            goods = Goods.objects.filter(is_active=True,from_id=from_id)
        except Exception as e:
            print('error ID!')
            return HttpResponse('error ID!')

        return render(request, 'market/dianpu.html', locals())
       


#获得所有食物类商品并输出给用户
def food(request):
    try:
        id = request.COOKIES.get("userid")
        user = Users.objects.get(id=id)
        goods = Goods.objects.filter(is_active=True, kinds = "食物")
        if user.isSeller:
            return render(request, 'sign/sign_in.html')
        else:
            return render(request, 'market/food.html',locals())
    except:

        return render(request, 'sign/sign_in.html') 

#获得所有服装类商品并输出给用户
def cloths(request):
    try:
        id = request.COOKIES.get("userid")
        user = Users.objects.get(id=id)
        goods = Goods.objects.filter(is_active=True, kinds = "服装")
        if user.isSeller:
            return render(request, 'sign/sign_in.html')
        else:
            return render(request, 'market/cloths.html',locals())
    except:

        return render(request, 'sign/sign_in.html') 

#获得所有数码类商品并输出给用户
def eproduct(request):
    try:
        id = request.COOKIES.get("userid")
        user = Users.objects.get(id=id)
        goods = Goods.objects.filter(is_active=True, kinds = "数码")
        if user.isSeller:
            return render(request, 'sign/sign_in.html')
        else:
            return render(request, 'market/eproducts.html',locals())
    except:

        return render(request, 'sign/sign_in.html') 

#购物车
def cart(request):
    try:
        id = request.COOKIES.get("userid")
        user = Users.objects.get(id=id)
        #购物车内的货物，尚未下单
        goods0 = SellGoods.objects.filter(is_active = True,to_id=id, status = 0)
        #获得详细信息并保存在列表中
        detailgoods0 = []
        for good0 in goods0:
            detailgood0 = Goods.objects.get(is_active = True,id = good0.good_id)
            detailgood0.createtime = good0.create_time
            detailgood0.sellid = good0.id
            detailgoods0.append(detailgood0)

        #已经下单未发货
        goods1 = SellGoods.objects.filter(is_active = True,to_id=id, status = 1)
        #获得详细信息并保存在列表中
        detailgoods1 = []
        for good1 in goods1:
            detailgood1 = Goods.objects.get(is_active = True,id = good1.good_id)
            detailgood1.num = good1.good_num
            detailgood1.createtime = good1.create_time
            detailgoods1.append(detailgood1)

        #发货未签收
        goods2 = SellGoods.objects.filter(is_active = True,to_id=id, status = 2)
        #获得详细信息并保存在列表中
        detailgoods2 = []
        for good2 in goods2:
            detailgood2 = Goods.objects.get(is_active = True,id = good2.good_id)
            detailgood2.num = good2.good_num
            detailgood2.sellid = good2.id
            detailgoods2.append(detailgood2)

        #成功签收的货物
        goods3 = SellGoods.objects.filter(is_active = True,to_id=id, status = 3)
        #获得详细信息并保存在列表中
        detailgoods3 = []
        for good3 in goods3:
            detailgood3 = Goods.objects.get(is_active = True,id = good3.good_id)
            detailgood3.num = good3.good_num
            detailgood3.edit_time = good3.edit_time
            detailgood3.sellid = good3.id
            detailgoods3.append(detailgood3)

        if user.isSeller:
            return render(request, 'sign/sign_in.html')
        else:
            return render(request, 'market/cart.html',locals())
    except:

        return render(request, 'sign/sign_in.html') 


#下单购物车中的货物
def fromcarttolist(request,good_id):
    try:
        good = SellGoods.objects.get(is_active = True,id=good_id)
    except Exception as e:
        print('error ID!')
        return HttpResponse('error ID!')
    good.status = 1
    good.save()
    return HttpResponseRedirect('/market/cart')

#签收商品
def signfor(request,good_id):
    try:
        good = SellGoods.objects.get(is_active = True,id=good_id)
    except Exception as e:
        print('error ID!')
        return HttpResponse('error ID!')
    good.status = 3
    good.save()
    return HttpResponseRedirect('/market/cart')


#从购物车中移除，也可用于删除订单
def removefromcart(request,good_id):
    try:
        good = SellGoods.objects.get(id=good_id)
    except Exception as e:
        print('error ID!')
        return HttpResponse('error ID!')
    good.is_active = 0
    good.save()
    return HttpResponseRedirect('/market/cart')

#添加评论，只有下单签收之后才可以评论
def addcomments(request,good_id):
    id = request.COOKIES.get("userid")
    user = Users.objects.get(id=id)
    good = Goods.objects.get(id=good_id)
    if request.method == 'GET':
        return render(request, 'market/comment.html', locals())

    elif request.method == 'POST':
        Comment.objects.create(good_id=good_id, to_id=id,text=request.POST['text'])

    return HttpResponseRedirect("/market/goodsdetail/"+str(good_id))