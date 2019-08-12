from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect, HttpResponse

import hashlib
from django.http import response

from .models import User


# import json

# Create your views here.
def index(request):
    # 假设 服务器判断request.cookie['session_id']。没有session_id没有或不正确禁止登录，重定向到登录
    return render(request, 'login/index.html', context={})


def register(request):
    """GET  返回注册表单"""
    if request.method == 'GET':
        return render(request, 'login/register.html', context={})
    elif request.method == 'POST':
        context = {}
        name = request.POST['name']
        password = request.POST['password']
        # 密码加密  # 也可以 form django.contrib.auth.ha
        md5 = hashlib.md5()
        md5.update(password.encode())
        hash_password = md5.hexdigest()

        # 验证 用户名、密码是否在长度范围内 len()      # 判断字符串纯中文 # 邮箱
        # if len(name) <= 1:
        #     # 讲ajax时的反例
        #     context['error_message']='用户名太短'
        #     return render(request,'login/register.html',context)
        # return render(request, 'login/register.html/', context)  # 失败

        user = User(name=name, password=password, hash_password=hash_password)
        user.save()
        return redirect(to='/login/index')  # 成功返回首页


def register_check(request):
    """检查注册参数，返回json结果
    :param   客户端的表单请求    name字段
    :method   请求方式  POST
    :return  json格式的字符串
    '
    {
        "code": 100,             # 200成功  100失败
        "status": "faild",       # ok成功
        "error_message": "",     # 用户名太短  等...
    }
    '

    """
    import json
    resp_obj = {}  # 响应对象
    name = request.POST['name']
    if len(name) <= 1:
        # 讲ajax时的反例
        resp_obj = {
            'code': 100,
            'status': '验证失败',
            'error_message': '用户名太短',
        }
        resp_json = json.dumps(resp_obj)
        print(type(resp_obj))
        print(type(resp_json))
        return HttpResponse(resp_json)


def do_register(request):
    pass


def login(request):
    if request.method == 'GET':
        return render(request, 'login/login.html', context={})
    elif request.method == 'POST':
        context = {}
        name = request.POST['name']
        password = request.POST['password']

        user_list = User.objects.filter(name=name, password=password)  # 多个where条件逗号分隔，代表and连接条件。
        # 多条件可以用Q对象，from django.db.models import  Q
        # User.objects.filter(Q=（name=1111）&Q(assword=1111))
        if user_list:
            # 登录成功
            request.session['is_login'] = True
            request.session['username'] = user_list[0].name
            request.COOKIES['is_login'] = True
            request.COOKIES['usename'] = user_list[0].name

            # 服务器要保留cookie，要设置set_cookie
            # response.set_cookie('is_login','True')
            # response.set_cookie('name','小明'.encode())

            context = {'message': '登录成功'}
            # return response
            # return render(request,'login/index.html',context)
            return redirect(to='/login/index/')
        else:
            # 登录失败
            if User.objects.filter(name=name).exists():
                context['message'] = '密码错误'
                return render(request, 'login/login.html', context={})
            else:
                context['message'] = '用户名不存在，请先注册'
                return render(request, 'login/login.html', context={})

    # def register_email_active():
    """用户提交注册信息后，需要邮件激活"""
    # 发一封邮件
    # user_name_encryp =user.id经过base64 或hash加密，形成新的字符串
    # active_url ='127.0.0.1:post' +'login/email_active/'+'user_name_encryp'


def do_login(request):
    pass


def logout(request):
    request.session.flush()  # 清除session
    # 统计在线人数，读Django_session表行数 自己测试注意用不同的浏览器登录
    return redirect('login/index/')


