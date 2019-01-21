from django.conf.urls import url
from django.contrib import admin
from .views import index_views,user_views,cate_views,goods_views

urlpatterns = [
	#路由	
    url(r'^$', index_views.index,name='myadmin_index'),
    #用户管理
    url(r'^vipuser/$', user_views.vipuser,name='myadmin_vipuser'),
    url(r'^adduser/$', user_views.adduser,name='myadmin_adduser'),
    url(r'^deluser/$', user_views.deluser,name='myadmin_deluser'),
    url(r'^edituser/$',user_views.edituser,name='myadmin_edituser'),
    url(r'^respwd/$',user_views.respwd,name='myadmin_respwd'),
    url(r'^changes/$', user_views.changes,name='myadmin_changes'),


    url(r'^addcate/$', cate_views.addcate,name='myadmin_addcate'),
    url(r'^catelist/$', cate_views.catelist,name='myadmin_catelist'),
    url(r'^delcate/$', cate_views.delcate,name='myadmin_delcate'),
    url(r'^editcate/$', cate_views.editcate,name='myadmin_editcate'),






    url(r'^addgoods/$',goods_views.addgoods,name='myadmin_addgoods'),
    url(r'^goodsinsert/$', goods_views.goodsinsert,name='myadmin_goodsinsert'),
    url(r'^goodslist/$',goods_views.goodslist,name='myadmin_goodslist'),
    url(r'^delgoods/$',goods_views.delgoods,name='myadmin_delgoods'),
    url(r'^editgoods/$',goods_views.editgoods,name='myadmin_editgoods'),









]
