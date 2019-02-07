from django.shortcuts import render,redirect
from django.contrib.auth.hashers import make_password, check_password
from django.http import HttpResponse,JsonResponse
from django.core.urlresolvers import reverse
from .. import models
from shop.settings import BASE_DIR
from django.core.paginator import Paginator
from django.contrib.auth.decorators import permission_required

# Create your views here.

def tab():
    cates = models.Cates.objects.extra(select = {'newpath':'concat(paths,id)'}).order_by('newpath')
    for i in cates:
        num = i.paths.count(',')-1
        i.newname=num*'|----'
    return cates    


@permission_required("myadmin.insert_cates",raise_exception = True)
def addcate(request):
	if request.method == 'GET':
		cates=models.Cates.objects.all()
		print(cates)
		return render(request,'myadmin/cate/addcate.html',{"cates":cates})
	elif request.method == 'POST':
		pid=request.POST.get('pid')
		name=request.POST.get('name')
		print(pid)
		print(name)
		if pid=='0':
			cate=models.Cates()
			cate.name=name
			cate.upid=int(pid)
			cate.paths='0,'
			cate.save()
		else: 
			pobj=models.Cates.objects.get(id=pid)
			c=models.Cates()
			c.name=name
			c.upid=pobj.id
			c.paths=pobj.paths+pid+','
			c.save()
		return HttpResponse(('<script>alert("添加成功");location.href="/myadmin/addcate/"</script>'))

@permission_required("myadmin.show_cates",raise_exception = True)
def catelist(request):
	cate = tab()
	# cate=models.Cates.objects.all()
	# print(cate)
	return render(request,'myadmin/cate/catelist.html',{"cate":cate})
	
@permission_required("myadmin.del_cates",raise_exception = True)
def delcate(request):
	pid = int(request.GET.get('pid'))
	count=models.Cates.objects.filter(upid=pid).count()
	if count :
		return JsonResponse({'msg':0})
	else :
		c = models.Cates.objects.get(id=pid)
		c.delete()
		return JsonResponse({'msg':1})
@permission_required("myadmin.edit_cates",raise_exception = True)
def editcate(request):
    # 接受id和name
    cid = int(request.GET.get('id'))
    cname = request.GET.get('name')
    try:
        cate = models.Cates.objects.get(id=cid)
        cate.name=cname
        cate.save()
        return JsonResponse({'msg':1})
    except :
        return JsonResponse({'msg':0})
