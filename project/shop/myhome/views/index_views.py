from django.shortcuts import render,redirect
from django.contrib.auth.hashers import make_password, check_password
from django.http import HttpResponse,JsonResponse
from django.core.urlresolvers import reverse
from myadmin import models
# Create your views here.
def index(request):
    cate =models.Cates.objects.all()
    

    goods=models.Goods.objects.all()

    content ={"cate":cate,"goods":goods}

    return render(request,'myhome/index.html',content)

def myhome_login(request):
    if request.method == "GET":
        return render(request,'myhome/login.html')

    elif request.method == "POST": 
        user= request.POST.dict()
        phone=user["account"] 
        cphone = models.Users.objects.filter(phone=phone).count()
        print(phone)
        if not cphone:
            return HttpResponse('<script>alert("你输入的手机号不存在,请注册");location.href="'+reverse('myhome_login')+'"</script>')
        else :
            users = models.Users.objects.filter(phone=phone)
            print(users)

            if  check_password(user['password'],users[0].password) :
                request.session['userinfo'] = [{"vipuser":users[0].username},{'uid':users[0].id}]
                return HttpResponse('<script>alert("登录成功");location.href="'+reverse('myhome_index')+'"</script>')
            else:
                return HttpResponse('<script>alert("你输入密码有误,请重新登录");location.href="'+reverse('myhome_login')+'"</script>')
 

def outlogin(request):
    try:
        del request.session['userinfo'] 
        return HttpResponse('<script>alert("退出登录");location.href="'+reverse('myhome_index')+'"</script>')
    except:
        return HttpResponse('<script>alert("退出登录");location.href="'+reverse('myhome_index')+'"</script>')
def myhome_register(request):
    if request.method == 'GET':
        return render(request,'myhome/register.html')
    elif request.method == 'POST':
        userinfo = request.POST.dict()
        if userinfo['username'] == '' or userinfo['phone'] == '' or userinfo['password'] == '':
            return HttpResponse('<script>alert("你的信息填写不完整");location.href="'+reverse("myhome_register")+'"</script>')

        flage = models.Users.objects.filter(phone=userinfo['phone']).count()
        if flage:
            return HttpResponse('<script>alert("手机好已经存在");history.back(-1)</script>')
        else:
            try:
                if userinfo['yzm'] == request.session['msgcode']['code'] and userinfo['phone'] == request.session['msgcode']['phone']:
        
                    newuser =models.Users()
                    newuser.username=userinfo['username'] 
                    newuser.phone=userinfo['phone'] 
                    newuser.password=make_password(userinfo['password'], None, 'pbkdf2_sha256')
                    newuser.sex = 1
                    newuser.age = 0
                    newuser.head_url ="/static/pics/1543425580.9038017.jpg"
                    newuser.save()
                    return HttpResponse('<script>alert("注册成功，请登录");location.href="'+reverse("myhome_login")+'"</script>')
                else:
                    return HttpResponse('<script>alert("验证码错误");history.back(-1)</script>')
            except:
                return HttpResponse('<script>alert("验证码错误");history.back(-1)</script>')
        

def sendmsg(request):
      
    # import urllib2
    import urllib
    import urllib.request
    import json
    import random
    #用户名 查看用户名请登录用户中心->验证码、通知短信->帐户及签名设置->APIID
    account  = "C87000499" 
    #密码 查看密码请登录用户中心->验证码、通知短信->帐户及签名设置->APIKEY
    password = "b485a61d820183a8058bf15b717e925b"
    mobile = request.GET.get('phone')
    # 随机验证码
    code = str(random.randint(10000,99999))
    # 把验证码存入session
    request.session['msgcode'] = {'code':code,'phone':mobile}
    # text = "您的验证码是："+code+"。请不要把验证码泄露给其他人。"
    # data = {'account': account, 'password' : password, 'content': text, 'mobile':mobile,'format':'json' }
    # req = urllib.request.urlopen(
    #     url= 'http://106.ihuyi.com/webservice/sms.php?method=Submit',
    #     data= urllib.parse.urlencode(data).encode('utf-8')
    # )
    # content =req.read()
    # res = json.loads(content.decode('utf-8'))
    print(code)
    # return HttpResponse(res)
    return JsonResponse({"code":code})