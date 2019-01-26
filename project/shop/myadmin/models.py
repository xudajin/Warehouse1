from django.db import models

# Create your models here.
from django.db import models

# Create your models here.
# 用户模型
class Users(models.Model):
    # 用户名  密码  手机号  性别 年龄 状态 添加时间  头像
	username = models.CharField(max_length=50)
	password = models.CharField(max_length=100)
	phone = models.CharField(max_length=11)
	sex = models.CharField(max_length=1)
	age = models.CharField(max_length=3)
	head_url = models.CharField(max_length=100)
    # 0 正常 1   2
	status = models.IntegerField(default=0)
	addtime=models.DateTimeField(auto_now_add=True)



# 商品的类别
class Cates(models.Model):  
    name = models.CharField(max_length=50)
    upid = models.IntegerField()
    paths = models.CharField(max_length=50)






class Goods(models.Model):
    # id titlt order_num status price img clicknum addtime 
    title = models.CharField(max_length=100)
    g_url = models.CharField(max_length=200)
    price = models.IntegerField()
    ordernum = models.IntegerField()
    ginfo = models.TextField()

    status = models.IntegerField(default=0)
    clicknum = models.IntegerField(default=0)
    addtime = models.DateTimeField(auto_now_add=True)

    cateid=models.ForeignKey(to="Cates",to_field="id")





class Car(models.Model):
    gid=models.ForeignKey(to="Goods",to_field="id")
    num = models.IntegerField()
    uid=models.ForeignKey(to="Users",to_field="id")






class Address(models.Model):
    # id   name phone sheng shi xian addinfo uid
    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=100)
    sheng = models.CharField(max_length=100)
    shi = models.CharField(max_length=100)
    xian = models.CharField(max_length=100)
    addinfo = models.CharField(max_length=255)

    uid=models.ForeignKey(to="Users",to_field="id")

    isselect = models.IntegerField(default=0)

class Citys(models.Model):
    name = models.CharField(max_length=100)
    level = models.IntegerField()
    upid = models.IntegerField()

    class Meta():
        db_table='citys'



# 订单
class Order(models.Model):
    # uid phone address    total wl pay uid status 
    uid = models.ForeignKey(to="Users",to_field="id") 
    phone = models.CharField(max_length=100)
    name = models.CharField(max_length=100)
    addinfo = models.CharField(max_length=255)
    total = models.IntegerField()
    # 0 顺丰 1 申通 2圆通
    wl = models.IntegerField()

    pay = models.IntegerField()

    status = models.IntegerField(default=0)

    createtime = models.DateTimeField(auto_now_add=True)

    paytime = models.DateTimeField(null=True)


class Orderinfo(models.Model):
    # gid  orderid num price
    orderid =  models.ForeignKey(to="Order",to_field="id")
    gid = models.ForeignKey(to="Goods",to_field="id")
    num = models.IntegerField()
    price = models.IntegerField()




