# -*- coding:UTF-8 -*-

from django.conf.urls import url
from . import views

app_name = 'webapp'

urlpatterns = [
    # url(r'^$', views.index, name='index'),
    # url(r'^login/$', views.login, name='login'),
    url(r'^$', views.login, name='login'),
    url(r'^index/$', views.index, name='index'),
    url(r'^checkuser/$', views.checkuser, name='checkuser'),
    url(r'^verifycode/$', views.verifycode, name='verifycode'),
    url(r'^add/$', views.add, name='add'),
    url(r'^list/$', views.list, name='list'),
]
