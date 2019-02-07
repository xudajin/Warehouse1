from django.shortcuts import render,redirect
from django.contrib.auth.hashers import make_password, check_password
from django.http import HttpResponse,JsonResponse
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User,Permission,Group


def useradd(request):
	if request.method == 'GET':

		glist = Group.objects.all()

		return render(request,'auth/user/add.html',{"glist":glist})

	elif request.method == 'POST':
		if request.POST['is_superuser'] == '1':
			ob = User.objects.create_superuser(request.POST['username'],request.POST['email'],request.POST['password'])
		else:
			ob = User.objects.create_user(request.POST['username'],request.POST['email'],request.POST['password'])
		ob.save()
		gs = request.POST.getlist('gs',None)
		if gs:
			ob.groups.set(gs)
			ob.save()

		return HttpResponse("<script>location.href='/myadmin/auth/user/list'</script>")


def userlist(request):
	data = User.objects.all()
	return render(request,'auth/user/list.html',{"data":data})


def groupadd(request):
	if request.method == 'GET':
		perms = Permission.objects.exclude(name__istartswith='Can')

		return render(request,'auth/group/add.html',{"perms":perms})
	
	elif request.method == 'POST':

		g= Group(name=request.POST['groupname'])
		g.save()
		perms = request.POST.getlist('perm',None)
		if perms:
			g.permissions.set(perms)
			g.save()
					
		return HttpResponse("<script>location.href='/myadmin/auth/group/list'</script>")


def grouplist(request):
	data = Group.objects.all()
	return render(request,'auth/group/list.html',{'glist':data})


def groupedit(request):
	gid = request.GET.get('id')
	ginfo = Group.objects.get(id=gid)
	if request.method == 'GET':
		perms = Permission.objects.exclude(name__istartswith='Can').exclude(group=ginfo)
		return render(request,'auth/group/edit.html',{'info':ginfo,"perms":perms})
	
	elif request.method == 'POST':
		ginfo.name == request.POST.get('groupname')
		perms = request.POST.getlist('perm',None)
		ginfo.permissions.clear()
		if perms:
			ginfo.permissions.set(perms)
		ginfo.save()
		return HttpResponse("<script>location.href='/myadmin/auth/group/list'</script>")

