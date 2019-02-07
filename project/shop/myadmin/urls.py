from django.conf.urls import url
from django.contrib import admin
from .views import index_views,user_views,cate_views,goods_views,auth_views

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


    url(r'^logoin/$', index_views.myadminLogin,name='myadmin_login'),
    url(r'^verifycode/$', index_views.verifycode,name='myadmin_yzm'),
    url(r'^outlogin/$', index_views.outlogin,name='myadmin_out'),

    url(r'^order/$', index_views.order,name='myadmin_order'),

    url(r'^auth/user/add$', auth_views.useradd,name='auth_user_add'),
    url(r'^auth/user/list$', auth_views.userlist,name='auth_user_list'),


    url(r'^auth/group/add$', auth_views.groupadd,name='auth_group_add'),
    url(r'^auth/group/list$', auth_views.grouplist,name='auth_group_list'),
    url(r'^auth/group/edit$', auth_views.groupedit,name='auth_group_edit'),






    










]
