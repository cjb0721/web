# coding:utf-8

import os,sys
import time
import pycurl
from .models import Monitor_data, Host_info
from django.conf import settings


def probe(url, id):
    # URL = 'https://www.baidu.com/'  # 探测的目标URL
    URL = url  # 探测的目标URL
    c = pycurl.Curl()  # 创建一个Curl对象
    c.setopt(pycurl.URL, URL)  # 定义请求的URL常量
    c.setopt(pycurl.CONNECTTIMEOUT, 5)  # 定义请求连接的等待时间
    c.setopt(pycurl.TIMEOUT, 5)  # 定义请求超时时间
    c.setopt(pycurl.NOPROGRESS, 1)  # 屏蔽下载进度条
    c.setopt(pycurl.MAXREDIRS, 1)  # 指定HTTP重定向的最大数为1
    c.setopt(pycurl.FORBID_REUSE, 1)  # 完成交互后强制断开连接，不重用
    c.setopt(pycurl.DNS_CACHE_TIMEOUT, 30)  # 设置保存DNS信息的时间为30秒

    # 创建一个文件对象，以“wb”方式打开，用来存储返回的http头部及页面的内容
    indexfile = open(settings.BASE_DIR + "/content.txt", "wb")
    c.setopt(pycurl.WRITEHEADER, indexfile)  # 将返回的HTTP HEADER定向到indexfile文件
    c.setopt(pycurl.WRITEDATA, indexfile)  # 将返回的HTML内容定向到indexfile文件

    c.perform()

    # try:
    #     c.perform()
    # except Exception, e:
    #     print "连接错误"
    #     indexfile.close()
    #     c.close()
    #     sys.exit()

    NAMELOOKUP_TIME = c.getinfo(c.NAMELOOKUP_TIME)  # DNS解析所消耗的时间
    CONNECT_TIME = c.getinfo(c.CONNECT_TIME)  # 建立连接所消耗的时间
    PRETRANSFER_TIME = c.getinfo(c.PRETRANSFER_TIME)  # 从建立连接到准备传输所消耗的时间
    STARTTRANSFER_TIME = c.getinfo(c.STARTTRANSFER_TIME)  # 从建立连接到传输开始消耗的时间
    TOTAL_TIME = c.getinfo(c.TOTAL_TIME)  # 传输结束所消耗的总时间
    HTTP_CODE = c.getinfo(c.HTTP_CODE)  # 返回HTTP状态码
    SIZE_DOWNLOAD = c.getinfo(c.SIZE_DOWNLOAD)  # 下载数据包的大小
    HEADER_SIZE = c.getinfo(c.HEADER_SIZE)  # HTTP头部大小
    SPEED_DOWNLOAD = c.getinfo(c.SPEED_DOWNLOAD)  # 平均下载速度
    REQUEST_SIZE = c.getinfo(c.REQUEST_SIZE)  # 请求包大小
    LENGTH_DOWNLOAD = c.getinfo(c.CONTENT_LENGTH_DOWNLOAD)  # 下载内容长度

    # 关闭Curl对象
    indexfile.close()
    c.close()


    host = Host_info.objects.get(pk=id)
    obj = Monitor_data()
    obj.fid = host
    obj.dns_lookup_time = NAMELOOKUP_TIME
    obj.connect_time = CONNECT_TIME
    obj.pre_transfer_time = PRETRANSFER_TIME
    obj.start_transfer_time = STARTTRANSFER_TIME
    obj.total_time = TOTAL_TIME
    obj.http_status = HTTP_CODE
    obj.size_download = SIZE_DOWNLOAD
    obj.size_header = HEADER_SIZE
    obj.size_request = REQUEST_SIZE
    obj.download_length = LENGTH_DOWNLOAD
    obj.download_speed = SPEED_DOWNLOAD
    obj.save()


