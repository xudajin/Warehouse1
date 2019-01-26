from django.shortcuts import render
from django.http import HttpResponse
from myadmin import models

# Create your views here.
def myhome_list(request,cid,bid):
	cate =models.Cates.objects.all()
	ob1 = models.Cates.objects.get(id=cid)
	ob2 =models.Cates. objects.filter(upid=cid)
	goods=[]
	bid = int(bid)
	for cate2 in ob2: # cate2   1   2           bid=2
        # 判断 如果点的事一级分类 cid=1 bid=0
		# cid = 1 bid = 11
		if cate2.id != bid and bid != 0:
			continue
        # 根据二级分类对象查询 当前一级分类下二级分类的所有商品
		goods.append(cate2.goods_set.all())

	content={'cate1':ob1,'cate2':ob2,'goods':goods,'color':bid,'cate':cate}

	return render(request,'myhome/list.html',content)