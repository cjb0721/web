from django.conf.urls import url
from . import views

app_name = 'webapp'

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^add/$', views.add, name='add'),
    url(r'^list/$', views.list, name='list'),
]
