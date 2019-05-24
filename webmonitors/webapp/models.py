# -*- coding:UTF-8 -*-

from django.db import models

# Create your models here.


# 主机表
class Host_info(models.Model):
    app_name = models.CharField(max_length=40)
    url = models.CharField(max_length=100)
    idc = models.CharField(max_length=4)
    alarm_type = models.CharField(max_length=8)
    alarm_info = models.CharField(max_length=30)

    def __str__(self):
        return self.app_name


# 监控数据表
class Monitor_data(models.Model):
    fid = models.ForeignKey('Host_info', on_delete=models.CASCADE)
    dns_lookup_time = models.FloatField()
    connect_time = models.FloatField()
    pre_transfer_time = models.FloatField()
    start_transfer_time = models.FloatField()
    total_time = models.FloatField()
    http_status = models.CharField(max_length=100)
    size_download = models.FloatField()
    size_header = models.SmallIntegerField()
    size_request = models.SmallIntegerField()
    download_length = models.FloatField()
    download_speed = models.FloatField()
    datetime = models.DateTimeField(auto_now_add=True, max_length=12)
    mark = models.IntegerField(default=0)

    def __str__(self):
        return "FID: "+str(self.fid.id)