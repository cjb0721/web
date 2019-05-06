from django.shortcuts import render, redirect, reverse
from django.http import HttpResponse
from django.conf import settings
from .models import *
import time

# Create your views here.


def index(request):
    # return render(request, 'webapp/index.html')
    system_name = settings.SYSTEM_NAME
    host_info_obj = Host_info.objects.order_by('app_name')

    if request.method == 'GET':
        return render(request, 'webapp/index.html', {'sys_name': system_name, 'host_info_obj': host_info_obj})
    elif request.method == 'POST':
        if request.POST['app_id']:
            # print("+++++++++++++++")
            # print(request.POST)
            # return HttpResponse("post请求")
            try:
                app_id = request.POST['app_id']
                host_info_row = Host_info.objects.filter(id=app_id)[0]
                if not 'start_time' in request.POST or request.POST['start_time'] == '':
                    start_time = int(str(time.time()).split('.')[0]) - 86400 * 3
                    end_time = int(str(time.time()).split('.')[0])
                    user_find = '0'
                    print("-------------")
                    # TODO 绘图
                else:
                    # start_time = int(time.mktime(time.strptime(request.POST['start_time'], '%Y-%m-%d %H:%M:%S')))
                    start_time = request.POST['start_time']
                    # end_time = int(time.mktime(time.strptime(request.POST['end_time'], '%Y-%m-%d %H:%M:%S')))
                    end_time = request.POST['end_time']
                    print(start_time, end_time)
                    user_find = '1'
                    print("+++++++++++++")
                    try:
                        r = 5 / 1
                        # TODO 绘图
                    except Exception as e:
                        info = ['系统提示：', '图型绘制失败,原因(' + str(e) + ')', '/webapp/']
                        return render(request, 'webapp/error.html', {'show_info': info})
                return render(request, 'webapp/index.html', {'sys_name': system_name, 'host_info_obj': host_info_obj,
                                                         'host_info_row': host_info_row, 'start_time': start_time,
                                                         'end_time': end_time, 'user_find': user_find})
            except Exception as e:
                info = ['系统提示：', str(e), '/webapp/']
                return render(request, 'webapp/error.html', {'show_info': info})
        else:
            print("======================")
            info = ['系统提示：', '未选择任何业务', '/webapp/']
            return render(request, 'webapp/error.html', {'show_info': info})


def add(request):
    idc_str = ""
    for k, v in settings.IDC.items():
        idc_str += "<input name='idc' type='checkbox' value=" + k + " id=" + k + "/>" + v + "\n"
    if request.method == 'GET':
        return render(request, 'webapp/add.html', {'IDC': idc_str})
    elif request.method == 'POST':
        # print(request.POST)

        appname = request.POST['appname']
        appurl = request.POST['appurl']
        hotice = request.POST['hotice']
        status = request.POST['status']
        responsechar = request.POST['responsechar']
        if responsechar:
            temp = responsechar
        else:
            temp = status
        if 'idc' in request.POST:
            idc = request.POST['idc']
            host_info_dict = {'app_name': appname, 'url': appurl, 'idc': idc, 'alarm_type': hotice, 'alarm_info': temp}
            try:
                host = Host_info.objects.create(**host_info_dict)
                # print(host)
                return redirect(reverse('webapp:index'))
            except Exception as e:
                info = ['系统提示：', e, '/webapp/']
                return render(request, 'webapp/error.html', {'show_info': info})

        else:
            info = ['系统提示：', '探测点不能为空', '/webapp/']
            return render(request, 'webapp/error.html', {'show_info': info})


