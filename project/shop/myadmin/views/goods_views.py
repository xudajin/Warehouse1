from django.shortcuts import render,redirect
from django.contrib.auth.hashers import make_password, check_password
from django.http import HttpResponse,JsonResponse
from django.core.urlresolvers import reverse
from .. import models
import time,os
from shop.settings import BASE_DIR
from django.core.paginator import Paginator
from . import cate_views,user_views
# Create your views here.


def addgoods(request):
    # 查询所有的分类  进行返回
    types = cate_views.tab()
    return render(request,'myadmin/goods/addgoods.html',{'types':types})

# 添加数据
def goodsinsert(request):
     # 接受用户的信息
    ginfo = request.POST.dict()
    ginfo.pop('csrfmiddlewaretoken')
    print(ginfo)

    file = request.FILES.get('g_url')
    if not file:
        return HttpResponse('<script>alert("请选择图片");history.back(-1)</script>')


    # 调图片上传
    g_url=user_views.upload(file)
    # 入库
    goods = models.Goods()
    goods.title=ginfo['title']
    goods.ordernum=ginfo['ordernum']
    goods.g_url=g_url
    goods.price=ginfo['price']
    goods.ginfo=ginfo['ginfo']
    goods.cateid=models.Cates.objects.get(id=ginfo['cateid'])
    goods.save()
    # 返回
    return HttpResponse('<script>alert("成功");location.href="/myadmin/goodslist/"</script>')

def goodslist(request):
	goodsinfo = models.Goods.objects.all()
	types = request.GET.get('type')
    # 接受关键字
	search = request.GET.get('search')
    # 判断用是否搜索内容
	if types:
		if types=='all':
            #根据id username phone
            # select * from myadmin_users where id like %search% or username like %search% or phone like %search%
			from django.db.models import Q
			goodsinfo = models.Goods.objects.filter(Q(title__contains=search)|Q(price__contains=search)|Q(ordernum__contains=search))
		elif types=='title':
			goodsinfo = models.Goods.objects.filter(title__contains=search)
		elif types=='price':
			goodsinfo = models.Goods.objects.filter(price__contains=search)
		elif types == 'ordernum':
			goodsinfo = models.Goods.objects.filter(ordernum__contains=search)

	 # 实例化分页对象
	p = Paginator(goodsinfo, 3)
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
	return render(request,'myadmin/goods/goodslist.html',{'goodsinfo':page1,'prange':prange,'page':page,'sumpage':sumpage})

def delgoods(request):
	gid =request.GET.get('id')
	print(gid)
	goods=models.Goods.objects.get(id=gid)
	goods.delete()
	return HttpResponse('<script>alert("删除成功");location.href="/myadmin/goodslist/"</script>')


def editgoods(request):
	gid =request.GET.get('id')

	if request.method =='GET':
		cates=cate_views.tab
		goods =models.Goods.objects.get(id=gid)
		print(goods.cateid_id)				
		return render(request,"myadmin/goods/editgoods.html",{"cates":cates,"goods":goods})
	elif request.method =='POST':
		newinfo = request.POST.dict()
		newinfo.pop('csrfmiddlewaretoken')
		print(newinfo)

		newgoods =models.Goods.objects.get(id=gid)
		newgoods.title=newinfo['title']
		newgoods.price=newinfo['price']
		newgoods.ordernum=newinfo['ordernum']
		newgoods.cateid_id=newinfo['cateid']
		newgoods.ginfo=newinfo['ginfo']
		file = request.FILES.get('g_url')
		if file:
			os.remove('.'+newgoods.g_url)
			gurl=upload(file)
			newgoods.g_url=gurl
		newgoods.save()
		return HttpResponse('<script>alert("修改成功");location.href="/myadmin/goodslist/"</script>')

	




def upload(myfile):

	filename = str(time.time())+"."+myfile.name.split('.').pop()
	destination = open("./static/pics/"+filename,"wb+")
	for chunk in myfile.chunks():      
		destination.write(chunk)  
	destination.close()
	return '/static/pics/'+filename