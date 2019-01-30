from django.shortcuts import render,redirect
from django.http import HttpResponse,JsonResponse
from myadmin import models
from django.core.urlresolvers import reverse
import time,os
# Create your views here.
def myhome_info(request):
	cate =models.Cates.objects.all()
	gid =request.GET.get("id")
	
	ginfo = models.Goods.objects.get(id=gid)

	return render(request,'myhome/goodsinfo.html',{"cate":cate,"ginfo":ginfo})

     # request.session['userinfo'] = [{"vipuser":users[0].username},{'uid':users[0].id}]

def addcar(request):
	try:
		info = request.GET.dict()
		gobj = models.Goods.objects.get(id=info['gid'])
		print(request.session["userinfo"][1]['uid'])
		uobj = models.Users.objects.get(id=request.session["userinfo"][1]['uid'])
		print(uobj)
		flag = models.Car.objects.filter(uid=uobj.id).filter(gid=gobj.id)
		if flag.count():
	        # 获取商品左更新
			for i in flag:
				i.num+=int(info['num'])
				i.save()
		else:
			car = models.Car()
			car.num=int(info['num'])
			car.gid=gobj
			car.uid=uobj
			car.save()
		return JsonResponse({"msg":1,'info':'添加成功'})
	except:
		return JsonResponse({"msg":1,'info':'添加失败'})
			

def carpage(request):
    # 查询当前用户的购物车
    uid = request.session.get('userinfo')
    if not uid:
        return HttpResponse('<script>alert("没有登录");location.href="'+reverse('myhome_login')+'"</script>')
    # # 查询用户
    user = models.Users.objects.get(id=uid[1]['uid'])
    # # 根据外建查询用户购物车里有多少商品
    cgoods = user.car_set.all()
    print(cgoods)
    # ,{'cgoods':cgoods}
    
    return render(request,'myhome/cart.html',{'cgoods':cgoods})



def caredit(request):
    # 接受数量和cid
    cinfo = request.GET.dict()
    # 根据id查询商品
    cobj = models.Car.objects.get(id=cinfo['cid'])
    # 修改数量
    cobj.num=int(cinfo['num'])
    cobj.save()

    return JsonResponse({'error':1,'msg':'修改成功'})



def delcar(request):
	delid = request.GET.get("delid")
	print(delid)
	cars =models.Car.objects.get(id=delid)
	cars.delete()

	return JsonResponse({'error':1,'msg':'删除成功'})



def confirm(request):
	login = request.session.get('userinfo')[0]['vipuser']

	cart=request.GET.get('cid').split(',')
	cargoods = models.Car.objects.filter(id__in=cart)

	citys =models.Citys.objects.filter(upid=0)

	userobj = models.Users.objects.get(id=request.session["userinfo"][1]['uid'])
	address =userobj.address_set.all()
	print(address)
	return render(request,'myhome/pay.html',{"login":login,"cargoods":cargoods,"citys":citys,'address':address})



def getcitys(request):
	upid = request.GET['upid']
	citys = models.Citys.objects.filter(upid=upid).values()
	return JsonResponse(list(citys),safe=False)


def saveaddress(request):

	addinfo = request.GET.dict()
	address = models.Address()
	addr = models.Address.objects.filter(uid=request.session["userinfo"][1]['uid']).count()
	print(addr)
	if addr == 0:
		address.isselect = 1
	else:
		address.isselect = 0

	address.name=addinfo['name']
	address.phone=addinfo['phone']
	address.sheng=models.Citys.objects.get(id=addinfo['sheng']).name
	address.shi=models.Citys.objects.get(id=addinfo['shi']).name
	address.xian=models.Citys.objects.get(id=addinfo['xian']).name
	address.addinfo=addinfo['addinfo']
	address.uid = models.Users.objects.get(id=request.session["userinfo"][1]['uid'])
	address.save()
	return JsonResponse({'error':0,'msg':'添加成功'})



def createorder(request):
	oinfo = request.POST.dict()
	print(oinfo)
	order = models.Order()
	order.uid =models.Users.objects.get(id=request.session["userinfo"][1]['uid'])
	order.phone = models.Address.objects.get(id=oinfo['dizhi']).phone
	order.name = models.Address.objects.get(id=oinfo['dizhi']).name
	
	sheng = models.Address.objects.get(id=oinfo['dizhi']).sheng
	shi = models.Address.objects.get(id=oinfo['dizhi']).shi
	xian = models.Address.objects.get(id=oinfo['dizhi']).xian
	addinfo = models.Address.objects.get(id=oinfo['dizhi']).addinfo
	print(addinfo)
	order.addinfo = sheng+shi+xian+addinfo

	order.wl = int(oinfo['wuliu'])
	order.pay = int(oinfo['zhifu'])

	order.total=0
	order.save()

	total = 0	
	carts = models.Car.objects.filter(id__in=oinfo['car'].split(','))
	for i in carts:
		orderinfo =models.Orderinfo()
		orderinfo.orderid = order
		orderinfo.num = i.num
		orderinfo.price = i.gid.price

		orderinfo.gid = i.gid
		orderinfo.save()
		total += i.num*i.gid.price
		i.delete()

	order.total = total
	order.save()
	return HttpResponse('<script>location.href="'+reverse('myhome_order_pay')+'?orderid='+str(order.id)+'"</script>')	


def myhome_order_pay(request):
    # 接收订单号
    orderid = request.GET.get('orderid')
    # 获取订单对象
    order = models.Order.objects.get(id=orderid)
    print(orderid)
    # 获取支付对象
    alipay = Get_AliPay_Object()

    # 生成支付的url
    query_params = alipay.direct_pay(
        subject="魅族旗舰官网",  # 商品简单描述
        out_trade_no = orderid,# 用户购买的商品订单号
        total_amount = order.total,  # 交易金额(单位: 元 保留俩位小数)
    )
    print(query_params)
    # 支付宝网关地址（沙箱应用）
    pay_url = settings.ALIPAY_URL+"?{0}".format(query_params)  
    print(pay_url)
    # 页面重定向到支付页面
    return redirect(pay_url)


# 支付的回调函数
# 支付宝回调地址
from django.views.decorators.csrf import csrf_exempt
@csrf_exempt
def myhome_pay_result(request):
    # 获取对象
    alipay = Get_AliPay_Object()
    if request.method == "POST":
        # 检测是否支付成功
        # 去请求体中获取所有返回的数据：状态/订单号
        from urllib.parse import parse_qs
        # name&age=123....
        body_str = request.body.decode('utf-8')
        post_data = parse_qs(body_str)

        post_dict = {}
        for k, v in post_data.items():
            post_dict[k] = v[0]

        sign = post_dict.pop('sign', None)
        status = alipay.verify(post_dict, sign)
        print('------------------开始------------------')
        print('POST验证', status)
        print(post_dict)
        out_trade_no = post_dict['out_trade_no']

        # 修改订单状态
        models.Order.objects.filter(id=out_trade_no).update(status=1)
        print('------------------结束------------------')
        # 修改订单状态：获取订单号
        return HttpResponse('POST返回')
    else:
        params = request.GET.dict()
        sign = params.pop('sign', None)
        status = alipay.verify(params, sign)
        print('==================开始==================')
        print('GET验证', status)
        print('==================结束==================')
        return HttpResponse('<script>alert("支付成功");支付完成</script>')


from shop import settings
from utils.pay import AliPay

# AliPay 对象实例化
def Get_AliPay_Object():
    alipay = AliPay(
        appid=settings.ALIPAY_APPID,# APPID （沙箱应用）
        app_notify_url=settings.ALIPAY_NOTIFY_URL, # 回调通知地址
        return_url=settings.ALIPAY_NOTIFY_URL,# 支付完成后的跳转地址
        app_private_key_path=settings.APP_PRIVATE_KEY_PATH, # 应用私钥
        alipay_public_key_path=settings.ALIPAY_PUBLIC_KEY_PATH,  # 支付宝公钥
        debug=True,  # 默认False,
    )
    return alipay












def deladdr(request):
	delid =request.GET.get('delid')
	print(delid)
	address = models.Address.objects.get(id=delid)
	address.delete()
	return JsonResponse({'error':0,'msg':'删除成功'})

def myself(request):
	uid = request.session.get('userinfo')
	if not uid:		
		return HttpResponse('<script>alert("没有登录");location.href="'+reverse('myhome_login')+'"</script>')
	else:
		pinfo = models.Users.objects.get(id=request.session["userinfo"][1]['uid'])
		return render(request,'myhome/personalcenter.html',{"pinfo":pinfo})



def myselfinfo(request):
	if request.method =="GET":
		pinfo = models.Users.objects.get(id=request.session["userinfo"][1]['uid'])
		print(pinfo.username)
		return render(request,'myhome/personalinfo.html',{"pinfo":pinfo})
	elif request.method == "POST":
		newinfo = request.POST.dict()
		print(newinfo)
		users = models.Users.objects.get(id=newinfo["uid"])
		users.username = newinfo["username"]
		users.age = newinfo["age"]
		users.sex = newinfo["sex"]
		users.phone = newinfo["phone"]

		try:
			file = request.FILES.get('head_url')
			print(file)
			if file:
				os.remove('.'+users.head_url)
				headurl=upload(file)
				users.head_url=headurl
			users.save()
		except:
			file = request.FILES.get('head_url')
			if file:
				headurl=upload(file)
				users.head_url=headurl
			users.save()

		return HttpResponse('<script>alert("修改成功");location.href="'+reverse('myhome_myselfinfo')+'"</script>')



def manageorder(request):
	users = models.Users.objects.get(id=request.session["userinfo"][1]['uid'])
	order = models.Order.objects.filter(uid=users)
	orderinfo =models.Orderinfo.objects.all()
	

	return render(request,'myhome/manageorder.html',{"order":order,"orderinfo":orderinfo})



def orderdetails(request):
	orderid =request.GET.get('orderid')
	order = models.Order.objects.get(id=orderid)
	orderinfo=order.orderinfo_set.all()
	print(orderinfo)

	return render(request,'myhome/orderdetails.html',{"orderinfo":orderinfo,"order":order})



def delorder(request):
	doid = request.GET.get('doid')
	delorder = models.Order.objects.get(id=doid)
	print(delorder.name)
	delorder.delete()
	return JsonResponse({"del":0,"msg":"删除成功"})



def setdefault(request):
	setid =request.GET.get("setid")
	print(setid)
	users = models.Users.objects.get(id=request.session["userinfo"][1]['uid'])
	addrinfo=users.address_set.all().update(isselect=0)
	print(addrinfo)
	select =models.Address.objects.get(id=setid)
	select.isselect = 1	
	select.save()

	return JsonResponse({"set":1})


def upload(myfile):

	filename = str(time.time())+"."+myfile.name.split('.').pop()
	destination = open("./static/pics/"+filename,"wb+")
	for chunk in myfile.chunks():      
		destination.write(chunk)  
	destination.close()
	return '/static/pics/'+filename




