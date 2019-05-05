from django.conf.urls import url
from . import views

app_name = 'webapp'

urlpatterns = [
    url('^$', views.index, name='index'),
]
