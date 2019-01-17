from django.shortcuts import render,redirect
from django.contrib.auth.hashers import make_password, check_password
from django.http import HttpResponse,JsonResponse
from django.core.urlresolvers import reverse
from . import models
import time,os
from shop.settings import BASE_DIR
from django.core.paginator import Paginator
# Create your views here.
def index(request):

	return render(request,'myadmin/index.html')


def vipuser(request):
	userinfo=models.Users.objects.all().exclude(status=3)

	types = request.GET.get('type')
    # 接受关键字
	search = request.GET.get('search')
    # 判断用是否搜索内容
	if types:
		if types=='all':
            #根据id username phone
            # select * from myadmin_users where id like %search% or username like %search% or phone like %search%
			from django.db.models import Q

			userinfo = models.Users.objects.filter(Q(id__contains=search)|Q(username__contains=search)|Q(phone__contains=search))
		elif types=='uname':
			userinfo = models.Users.objects.filter(username__contains=search)
		elif types=='uphone':
			userinfo = models.Users.objects.filter(phone__contains=search)
		elif types == 'uid':
			userinfo = models.Users.objects.filter(id__contains=search)


	 # 实例化分页对象
	p = Paginator(userinfo, 10)

    #一共可以分多少页
	sumpage=p.num_pages

    # 取第几页的数据
    # 接受用户的页码
	page = int(request.GET.get('p',1))
    # 第几页的数据
	page1 = p.page(page)

    # 判断 如果用输入的页码<=3 显示前五个页码
	if page<=3:
        # 页码的迭代序列  [1,2,3,4,5,6,7]
		prange = p.page_range[:5]
	elif page+2>=sumpage:
		prange = p.page_range[-5:]
	else:
		prange = p.page_range[page-3:page+2]
	return render(request,'myadmin/table-list.html',{'userinfo':page1,'prange':prange,'page':page,'sumpage':sumpage})


def adduser(request):
	if request.method=='GET':
		return render(request,'myadmin/adduser.html')
	elif request.method=='POST':
		userinfo = request.POST.dict()
		userinfo.pop('csrfmiddlewaretoken')

		myfile = request.FILES.get("head_url",None)
	 
		if not myfile:
			return HttpResponse("<script>alert('请选择头像');location.href=''</script>")
		userinfo['head_url']=upload(myfile)
	 
		userinfo['password'] = make_password(userinfo['password'], None, 'pbkdf2_sha256')
		try:
			user = models.Users(**userinfo)
			user.save()
			return redirect(reverse('myadmin_vipuser'))
		except :
			return HttpResponse("<script>alert('失败！');location.href=''</script>")

def deluser(request):
	uid=request.GET.dict()
	uid=uid["id"]
	print(uid)
	userinfo =models.Users.objects.get(id=uid)
	userinfo.status= 3
	userinfo.save()
	return HttpResponse("删除成功")


def edituser(request):
	uid=request.GET.get("id")
	if request.method == 'GET':
		userinfo =models.Users.objects.get(id=uid)
		return render(request,"myadmin/edituser.html",{"u":userinfo})
	elif request.method == 'POST':
		userinfo=request.POST.dict()
		print(userinfo)
		uinfo=models.Users.objects.get(id=uid)
		uinfo.username=userinfo['username']
		uinfo.phone=userinfo['phone']
		uinfo.age=userinfo['age']
		uinfo.sex=userinfo['sex']

		file = request.FILES.get('head_url')
		if file:
			os.remove('.'+uinfo.head_url)
			headurl=upload(file)
			uinfo.head_url=headurl
		uinfo.save()
		return HttpResponse('修改成功')



def respwd(request):
	uid=request.GET.get("id")
	user=models.Users.objects.get(id=uid)
	user.password = make_password('123456', None, 'pbkdf2_sha256')
	user.save()
	return HttpResponse(("<script>alert('重置成功！');location.href='/vipuser/'</script>"))

def changes(request):
    # 获取uid 获取状态值
	uid = request.GET.get('uid')
	status = request.GET.get('status')
	try:
		user = models.Users.objects.get(id=uid)
		user.status=int(status)
		user.save()
		msg={'msg':'修改成功'}
		return JsonResponse(msg)
	except:
		msg={'msg':'修改失败'}
		return JsonResponse(msg)

		
def upload(myfile):
	
	filename = str(time.time())+"."+myfile.name.split('.').pop()
	destination = open("./static/pics/"+filename,"wb+")
	for chunk in myfile.chunks():      
		destination.write(chunk)  
	destination.close()
	return '/static/pics/'+filename
