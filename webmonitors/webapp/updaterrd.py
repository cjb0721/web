# -*- coding: utf-8 -*-
import os, sys
import django
import time
import pycurl
import rrdtool
import string
# import MySQLdb

import logging

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "webmonitors.settings")
django.setup()

import config
from webapp.models import *


class UpdateRRD():
    # 初始化
    def __init__(self):
        # 初始化日志对象
        logging.basicConfig(level=logging.DEBUG,
                            format='%(asctime)s [%(levelname)s] %(message)s',
                            filename= os.path.dirname(os.path.realpath(__file__)) + '/syslog.log',
                            filemode='a')

        # # 连接数据
        # try:
        #     self.conn = MySQLdb.Connection(DBHOST, DBUSER, DBPASSWORD, DBNAME)
        #     self.cursor = self.conn.cursor(MySQLdb.cursors.DictCursor)
        # except Exception, e:
        #     logging.error('connect database error!' + str(e))
        #     return

        self.rrdfiletype = ['time', 'download', 'unavailable']

    # # 虚构方法
    # def __del__(self):
    #     try:
    #         self.cursor.close()
    #         self.conn.close()
    #     except Exception, e:
    #         logging.debug('__del__ object error!' + str(e))

    # 更新rrd文件
    def updateRRD(self, rowobj):
        print ("==========================>>>updateRRD", rowobj.http_status)
        if str(rowobj.http_status) == "200":
            unavailablevalue = 0
        else:
            unavailablevalue = 1
        FID = rowobj.fid.id

        print ("++++++++++++++++++++++++++++++++++++++")
        print (unavailablevalue)
        print (rowobj.fid.id)
        print ("++++++++++++++++++++++++++++++++++++++")

        time_rrdpath = config.RRD_PATH + '/' + str(self.getURL(FID)) + '/' + str(FID) + '_' + str(self.rrdfiletype[0]) + '.rrd'
        download_rrdpath = config.RRD_PATH + '/' + str(self.getURL(FID)) + '/' + str(FID) + '_' + str(
            self.rrdfiletype[1]) + '.rrd'
        unavailable_rrdpath = config.RRD_PATH + '/' + str(self.getURL(FID)) + '/' + str(FID) + '_' + str(
            self.rrdfiletype[2]) + '.rrd'

        print (FID)
        print (time_rrdpath)
        print (download_rrdpath)
        print (unavailable_rrdpath)

        try:
            temp = rrdtool.updatev(time_rrdpath, '%s:%s:%s:%s:%s:%s' % (
            str(rowobj.datetime), str(rowobj.dns_lookup_time), str(rowobj.connect_time),
            str(rowobj.pre_transfer_time), str(rowobj.start_transfer_time), str(rowobj.total_time)))

            temp1 = rrdtool.updatev(download_rrdpath, '%s:%s' % (str(rowobj.datetime), str(rowobj.download_speed)))
            temp2 = rrdtool.updatev(unavailable_rrdpath, '%s:%s' % (str(rowobj.datetime), str(unavailablevalue)))

            self.setMARK(rowobj.id)

            print("------------------------------------------------------------>>")
            print (temp)
            print (temp1)
            print (temp2)
            print("------------------------------------------------------------>>")

            print (str(rowobj.datetime), str(rowobj.dns_lookup_time), str(rowobj.connect_time),
            str(rowobj.pre_transfer_time), str(rowobj.start_transfer_time), str(rowobj.total_time))
            # print (rowobj.size_header)

        except Exception, e:
            logging.error('Update rrd error:' + str(e))

    # 更新已标志记录
    def setMARK(self, _id):
        try:

            monitor = Monitor_data.objects.get(pk=_id)
            monitor.mark = 1
            monitor.save()

            # self.cursor.execute("update webmonitor_monitordata set MARK='1' where ID='%s'" % (_id))
            # self.conn.commit()
        except Exception, e:
            logging.error('SetMark datebase  error:' + str(e))

    # 获取未标志的新记录
    def getNewdata(self):
        print ("===================>>>getNewdata")
        try:
            monitor = Monitor_data.objects.filter(mark=0)
            print ("===================>>>monitor", monitor)
            for row in monitor:
                print (row.mark)
                self.updateRRD(row)

            # self.cursor.execute(
            #     "select ID,FID,NAMELOOKUP_TIME,CONNECT_TIME,PRETRANSFER_TIME,STARTTRANSFER_TIME,TOTAL_TIME,HTTP_CODE,SPEED_DOWNLOAD,DATETIME from webmonitor_monitordata where MARK='0'")
            # for row in self.cursor.fetchall():
            #     self.updateRRD(row)
        except Exception as e:
            print ("ERROR1")
            logging.error('Get new database  error:' + str(e))

    # 获取域名
    def getURL(self, _id):
        try:
            print ("=========================>>>getURL", _id)
            host = Host_info.objects.get(pk=_id)
            url = host.url
            print (url)
            return self.GetURLdomain(url)

            # self.cursor.execute("select URL from webmonitor_hostinfo where ID='%s'" % (_id))
            # return self.GetURLdomain(self.cursor.fetchall()[0]["URL"])
        except Exception, e:
            logging.error('Get FID URL  error:' + str(e))

    # 获取URL域名
    def GetURLdomain(self, url):
        xurl = ""
        if url[:8] == "https://":
            xurl = url[8:]
        else:
            xurl = url
        return string.split(xurl, '/')[0]


if __name__ == '__main__':
    app = UpdateRRD()
    app.getNewdata()
    print ("===================================>updaterrd")