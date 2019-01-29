from django.shortcuts import render
from django.http import HttpResponse,JsonResponse
from myadmin import models
from django.core.urlresolvers import reverse
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
	return HttpResponse('<script>alert("ok");location.href="'+reverse('myhome_manageorder')+'"</script>')
	

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
