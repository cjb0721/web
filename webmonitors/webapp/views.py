# -*- coding:UTF-8 -*-

from django.shortcuts import render, redirect, reverse
from django.http import HttpResponse
from django.conf import settings
from .models import *
import time, pycurl, random, io
from . import webprobe
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from PIL import Image, ImageFont, ImageDraw
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.core.mail import send_mail, send_mass_mail

from publicapp.views import *

# Create your views here.


def index(request):
    # return render(request, 'webapp/index.html')
    system_name = settings.SYSTEM_NAME
    host_info_obj = Host_info.objects.order_by('app_name')

    if authenticate(username=request.session.get('name'), password=request.session.get('pass')):
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
                    # print (host_info_row.url)
                    webprobe.probe(host_info_row.url, app_id)
                    if not 'start_time' in request.POST or request.POST['start_time'] == '':
                        start_time = int(str(time.time()).split('.')[0]) - 86400 * 3
                        end_time = int(str(time.time()).split('.')[0])
                        user_find = '0'
                        print("-------------")
                        result = Graphrrd_normal(host_info_row.id, host_info_row.url, host_info_row.app_name)
                        # print (result, type(result))
                    else:
                        # start_time = int(time.mktime(time.strptime(request.POST['start_time'], '%Y-%m-%d %H:%M:%S')))
                        start_time = request.POST['start_time']
                        # end_time = int(time.mktime(time.strptime(request.POST['end_time'], '%Y-%m-%d %H:%M:%S')))
                        end_time = request.POST['end_time']
                        # print(start_time, end_time)
                        user_find = '1'
                        print("+++++++++++++")
                        try:
                            # r = 5 / 1
                            result = Graphrrd_custom(host_info_row.id, start_time, end_time, host_info_row.url, host_info_row.app_name)
                        except Exception as e:
                            info = ['系统提示：', '图型绘制失败,原因(' + str(e) + ')', '/webapp/index']
                            return render(request, 'webapp/error.html', {'show_info': info})
                    return render(request, 'webapp/index.html', {'sys_name': system_name, 'host_info_obj': host_info_obj,
                                                             'host_info_row': host_info_row, 'start_time': start_time,
                                                             'end_time': end_time, 'user_find': user_find, 'url': str(result['url']),
                                                                 'num': str(result['num'])})
                except Exception as e:
                    info = ['系统提示：', str(e), '/webapp/index']
                    return render(request, 'webapp/error.html', {'show_info': info})
            else:
                print("======================>None")
                info = ['系统提示：', '未选择任何业务', '/webapp/index']
                return render(request, 'webapp/error.html', {'show_info': info})
    else:
        return redirect(reverse('webapp:login'))


def add(request):
    idc_str = ""
    for k, v in settings.IDC.items():
        idc_str += "<input name='idc' type='checkbox' value=" + k + " id=" + k + "/>" + v + "\n"
    if request.method == 'GET':
        return render(request, 'webapp/add.html', {'IDC': idc_str})
    elif request.method == 'POST':
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
                # return redirect(reverse('webapp:index'))

                try:
                    if not os.path.isdir(settings.RRD_PATH + '/' + GetURLdomain(appurl)):
                        os.makedirs(settings.RRD_PATH + '/' + GetURLdomain(appurl))

                    if not os.path.isdir(settings.PNG_PATH + '/' + GetURLdomain(appurl)):
                        os.makedirs(settings.PNG_PATH + '/' + GetURLdomain(appurl))

                except Exception as e:
                    return HttpResponse("目录创建失败！" + str(e))

                try:
                    create_rrd(str(appurl))
                except Exception as e:
                    return HttpResponse("目录RRD文件失败！" + str(e))

                info = ['系统提示：', '祝贺你，应用添加成功！请返回', '/webapp/index']
                return render(request, 'webapp/error.html', {'show_info': info})
            except Exception as e:
                info = ['系统提示：', e, '/webapp/index']
                return render(request, 'webapp/error.html', {'show_info': info})

        else:
            info = ['系统提示：', '探测点不能为空', '/webapp/index']
            return render(request, 'webapp/error.html', {'show_info': info})


def list(request):
    try:
        app_id = request.GET['app_id']
        start_time = request.GET['start_time']
        end_time = request.GET['end_time']
        # print(app_id, start_time, end_time)
        # print(type(Monitor_data.objects.filter(fid=app_id)[0]))
        # contact_list = Monitor_data.objects.filter(fid=app_id).filter(datetime__gte=start_time).filter(datetime__lte=end_time).order_by("-datetime")
        contact_list = Monitor_data.objects.filter(fid=app_id).order_by("-datetime")
        # print("====================>", contact_list)
        # 分页
        pageinator = Paginator(contact_list, 5)
        num = request.GET.get('page')
        try:
            page = pageinator.page(num)
        except PageNotAnInteger:
            page = pageinator.page(1)
        except EmptyPage:
            page = pageinator.page(pageinator.num_pages)

        return render(request, 'webapp/list.html', {'pages': page, 'app_id':app_id,'start_time':start_time,'end_time':end_time})
    except Exception as e:
        return render(request, 'webapp/list.html')


def login(request):
    if request.method == 'POST':
        try:
            username = request.POST['username']
            password = request.POST['password']
            request.session['name'] = username
            request.session['pass'] = password
            request.session.set_expiry(3600)
            verify = request.POST['verify'].lower()
            verifycode = request.session.get('verifycode').lower()

            if verify == verifycode:
                if authenticate(username=request.session.get('name'), password=request.session.get('pass')):
                    return redirect(reverse('webapp:index'))
                else:
                    return redirect(reverse('webapp:login'))
            else:
                print ("验证码错误")
                return render(request, 'webapp/login.html')
        except Exception as e:
            print (e)

    return render(request, 'webapp/login.html')


def checkuser(request):
    if request.method == 'POST':
        username = request.POST['username']
        user = User.objects.filter(username=username).first()
        if user is None:
            return HttpResponse("用户名错误")
        else:
            return HttpResponse("accept")


def verifycode(request):
    # 生成一张验证码图片
    # 定义变量，用于画面的背景色、宽、高
    bgcolor = (random.randrange(20, 100), random.randrange(20, 100), random.randrange(20, 100))
    width = 93
    heigth = 50
    # 创建画面对象
    im = Image.new('RGB', (width, heigth), bgcolor)
    # 创建画笔对象
    draw = ImageDraw.Draw(im)
    # 调用画笔的point()函数绘制噪点
    for i in range(0, 100):
        xy = (random.randrange(0, width), random.randrange(0, heigth))
        fill = (random.randrange(0, 255), 255, random.randrange(0, 255))
        draw.point(xy, fill=fill)
    # 定义验证码的备选值
    str1 = 'ABCD123EFGHIJK456LMNOPQRS789TUVWXYZ0'
    # 随机选取4个值作为验证码
    rand_str = ''
    for i in range(0, 4):
        rand_str += str1[random.randrange(0, len(str1))]
    # 构造字体对象
    # font = ImageFont.truetype('SCRIPTBL.TTF', 23)
    font = ImageFont.truetype('/usr/share/fonts/MAGNETOB.TTF', 24)
    fontcolor = (255, random.randrange(0, 255), random.randrange(0, 255))
    # 绘制4个字
    draw.text((5, 13), rand_str[0], font=font, fill=fontcolor)
    draw.text((25, 13), rand_str[1], font=font, fill=fontcolor)
    draw.text((50, 13), rand_str[2], font=font, fill=fontcolor)
    draw.text((75, 13), rand_str[3], font=font, fill=fontcolor)

    # 释放画笔
    del draw
    # 将生成的验证码存入session
    request.session['verifycode'] = rand_str
    print(rand_str)
    f = io.BytesIO()
    im.save(f, 'png')
    # 将内存中的图片数据返回给客户端，MIME类型为图片png
    return HttpResponse(f.getvalue(), 'image/png')


def find(request):

    if request.method == 'GET':
        return render(request, 'webapp/verifyuser.html')
    elif request.method == 'POST':
        try:
            username = request.POST['username']
            verify = request.POST['code'].lower()
            verifycode = request.session.get('verifycode').lower()

            if verify == verifycode:
                result = User.objects.filter(username=username)
                if result:
                    return render(request, 'webapp/sendmail.html', {'username': username})
                else:
                    print ("账户不存在")
                    return redirect(reverse('webapp:find'))
            else:
                print ("验证码错误")
                return redirect(reverse('webapp:find'))
        except Exception as e:
            print (e)
            return redirect(reverse('webapp:find'))




def mail(request):
    if request.method == 'GET':
        return render(request, 'webapp/sendmail.html')
    elif request.method == 'POST':
        try:
            sendemail = settings.DEFAULT_FROM_EMAIL
            username = request.POST['username']
            useremail = request.POST['useremail']
            verify = request.POST['code'].lower()
            verifycode = request.session.get('verifycode').lower()

            if verify == verifycode:
                # try:
                res = send_mail(username, username+'账户密码忘记，需要找回密码', sendemail, [useremail,])
                print (res)
                print ("发送成功")
                return render(request, 'webapp/sending.html')
                # except Exception as e:
                #     print ("发送失败", e)
                #     return redirect(reverse('webapp:find'))
            else:
                print ("验证码错误")
                return redirect(reverse('webapp:find'))
        except Exception as e:
            print (e)
            return redirect(reverse('webapp:find'))



def send(request):
    return render(request, 'webapp/sending.html')


def result(request):
    return render(request, 'webapp/sendsuccess.html')


