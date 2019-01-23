from django.conf.urls import url
from django.contrib import admin
from . views import index_views,list_views,info_views

urlpatterns = [
    url(r'^$', index_views.index,name='myhome_index'),
    
    url(r'^login/$', index_views.myhome_login,name='myhome_login'),
    url(r'^register/$', index_views.myhome_register,name='myhome_register'),
    url(r'^sendmsg/$', index_views.sendmsg,name='myhome_sendmsg'),
    url(r'^outlogin/$', index_views.outlogin,name='myhome_out'),




    url(r'^list/(?P<cid>[0-9]+)/(?P<bid>[0-9]+)/$', list_views.myhome_list,name='myhome_list'),

    
    url(r'^info/$', info_views.myhome_info,name='myhome_info'),




    












]
