from django.shortcuts import render,redirect
from django.contrib.auth.hashers import make_password, check_password
from django.http import HttpResponse
from django.core.urlresolvers import reverse
from . import models
import time,os
# Create your views here.
def index(request):
	return render(request,'myadmin/index.html')


def vipuser(request):
	return render(request,'myadmin/table-list.html')



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
            return HttpResponse("<script>alert('添失败！');location.href=''</script>")


def upload(myfile):
    
	filename = str(time.time())+"."+myfile.name.split('.').pop()
	destination = open("./static/pics/"+filename,"wb+")
	for chunk in myfile.chunks():      
		destination.write(chunk)  
	destination.close()
	return '/static/pics/'+filename

	