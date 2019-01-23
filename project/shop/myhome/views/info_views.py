from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def myhome_info(request):
	return render(request,'myhome/goodsinfo.html')
