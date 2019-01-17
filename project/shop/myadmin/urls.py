from django.conf.urls import url
from django.contrib import admin
from . import views

urlpatterns = [
    url(r'^$', views.index,name='myadmin_index'),
    url(r'^vipuser/$', views.vipuser,name='myadmin_vipuser'),
    url(r'^adduser/$', views.adduser,name='myadmin_adduser'),
    url(r'^deluser/$', views.deluser,name='myadmin_deluser'),
    url(r'^edituser/$',views.edituser,name='myadmin_edituser'),
    url(r'^respwd/$',views.respwd,name='myadmin_respwd'),
    url(r'^changes/$', views.changes,name='myadmin_changes'),




]
