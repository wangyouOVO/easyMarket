from django.db import models

# Create your models here.
from django.db import models

#在此建立数据库中的三个表单

#所有上架货物
class Goods(models.Model):
    name = models.CharField('商品名', max_length=50, default='')
    img = models.CharField('图片', max_length=50, default='')
    kinds = models.CharField('种类', max_length=50, default='')
    discribe = models.TextField('描述', max_length=100, default='')
    price = models.DecimalField('价格', max_digits=7, decimal_places=2, default=0)
    from_id = models.IntegerField('商家ID', default=1)
    is_recommend = models.BooleanField('是否推荐', default=False)
    is_active = models.BooleanField('是否存在', default=True)
    create_time = models.DateTimeField('创建时间', auto_now_add=True)
    edit_time = models.DateTimeField('更新时间', auto_now=True)
    # imgs = models.FileField(upload_to='static/product_images')
    def __str__(self):
        return "%s" % (self.name)

#所有用户
class Users(models.Model):
    name = models.CharField('用户名', max_length=50, default='')
    passWord = models.CharField('密码', max_length=50, default='')
    eMail = models.CharField('邮件', max_length=50, default='')
    location = models.CharField('地址', max_length=50, default='')
    is_active = models.BooleanField('是否存在', default=True)
    isSeller = models.BooleanField('是否为商家', default=False)

    def __str__(self):
        return "%s" % (self.name)

#所有订单
class SellGoods(models.Model):
    good_id=models.IntegerField('货物ID',default=1)
    
    from_id=models.IntegerField('商家ID',default=1)
    to_id=models.IntegerField('用户ID',default=1)
    status=models.IntegerField('状态码',default=0)
    # 0:仅仅加入购物车； 1：下单未发货；2：发货未接收 ；3：发货且接收
    create_time= models.DateTimeField('创建时间',auto_now_add=True) 
    edit_time= models.DateTimeField('更新时间',auto_now=True)
    good_num = models.IntegerField('下单数量',default=1)
    is_active = models.BooleanField('是否存在', default=True)
    def __str__(self):
        return "%s"%(self.name)

#所有评论
class Comment(models.Model):
    good_id=models.IntegerField('货物ID',default=1)
    #哪个用户发表的评论
    to_id=models.IntegerField('用户ID',default=1)
    text=models.CharField('地址', max_length=100, default='')
    edit_time= models.DateTimeField('更新时间',auto_now=True)
    create_time= models.DateTimeField('创建时间',auto_now_add=True) 
    is_active = models.BooleanField('是否存在', default=True)
    def __str__(self):
        return "%s"%(self.name)
