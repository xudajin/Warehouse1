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
    return HttpResponse('<script>alert("成功");location.href="/goodslist/"</script>')

def goodslist(request):
	goodsinfo = models.Goods.objects.all()
	return render(request,"myadmin/goods/goodslist.html",{"goodsinfo":goodsinfo})

def delgoods(request):
	gid =request.GET.get('id')
	print(gid)
	goods=models.Goods.objects.get(id=gid)
	goods.delete()
	return HttpResponse('<script>alert("删除成功");location.href="/goodslist/"</script>')


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
		return HttpResponse('<script>alert("修改成功");location.href="/goodslist/"</script>')

	









def upload(myfile):

	filename = str(time.time())+"."+myfile.name.split('.').pop()
	destination = open("./static/pics/"+filename,"wb+")
	for chunk in myfile.chunks():      
		destination.write(chunk)  
	destination.close()
	return '/static/pics/'+filename