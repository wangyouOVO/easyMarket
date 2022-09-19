from tkinter import EXCEPTION
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseNotModified
from .models import Goods, Users 
import hashlib
from django.contrib import messages
from django.core.exceptions import ValidationError


# Create your views here.

#登陆
def sign_in(request):
    if request.method == "GET":
        '''
          对用户和商家进行判断，免登陆  '''
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
        ##########  对用户和商家进行判断，免登陆   ############

    elif request.method == "POST":
        email = request.POST['eMail']
        pwd = request.POST['pwd']
        try:
            user = Users.objects.get(eMail=email)
        except EXCEPTION as e:
            return HttpResponse('登陆失败')
        m = hashlib.md5()
        m.update(pwd.encode())
        pwd_m = m.hexdigest()
        if user.passWord != pwd_m:
            return render(request, 'sign/sign_in.html', {'error_pwd': '密码错误，请重新输入'})
        else:
            request.session['user_email'] = email
            request.session['userid'] = user.id
            goods = Goods.objects.filter(is_active=True, is_recommend = True)
            if user.isSeller:
                ans = 'sale/goods.html'
            else:
                ans = 'market/recommend.html'
            ret = render(request, ans, locals())
            if 'remember' in request.POST:
                ret.set_cookie('user_email', email, 3600 * 24 * 3)
                ret.set_cookie('userid', user.id, 3600 * 24 * 3)
            return ret
            # return HttpResponse('登陆成功')

#注册
def sign_up(request):
    if request.method == "GET":
        return render(request, 'sign/sign_in.html')

    elif request.method == "POST":
        email = request.POST['email']
        passWord = request.POST['pwd']
        passWord2 = request.POST['pwd2']
        if passWord2 != passWord:
            return render(request, 'sign/sign_up.html', {'diff_pwd': '两次密码输入不一致'})
        old_name = Users.objects.filter(eMail=email)
        if old_name:
            return render(request, 'sign/sign_up.html', {'exist_email': '该邮箱已经被注册过啦~'})

        m = hashlib.md5()
        m.update(passWord.encode())
        passWord_m = m.hexdigest()

        user = Users.objects.create(name=request.POST['name'], passWord=passWord_m, eMail=request.POST['email'],
                                    location=request.POST['location'])

        request.session['user_email'] = email
        request.session['userid'] = user.id
        ##################################
        if 'remember1' in request.POST:
            user.isSeller = 'True'
            user.save()
            # ret.set_cookie('isSeller','Ture'.id,3600*24*3)
        if user.isSeller:
            ans = 'sale/admin.html'
        else:
            ans = 'market/recommend.html'
        ret = render(request, ans,locals())
       
        if 'remember' in request.POST:
            ret.set_cookie('user_email', email, 3600 * 24 * 3)
            ret.set_cookie('userid', user.id, 3600 * 24 * 3)
        return ret

#退出登陆
def delete_sign(request):
    try:
        id = request.COOKIES.get("userid")
        if id:
            ans = render(request, 'sign/sign_in.html')
            ans.delete_cookie('userid')
            return render(request, ans)
    except:
        return render(request, 'sign/sign_in.html')
