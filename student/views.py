import os
from math import ceil
from django.http import HttpResponseRedirect,HttpResponse
from django.shortcuts import render
from django.db.models import Max
from student import models
from .models import Student,Class   # from .models import   # from . import models
from pyexcel_io import save_data
import json

# Create your views here.
def index(request):
    """获取学生列表"""
    # page_no=2  page_size=3
    # 计算分页索引
    page_no = int(request.GET.get('page_no', 1))
    page_size = int(request.GET.get('page_size', 3))
    start_index = (page_no - 1) * page_size
    end_index = page_no * page_size

    # todo 多条件过滤思路
    # q1=Q()   用Q不好实现，参数可能有可能没有
    # q2=",gender=1"
    # Student.object.filter(q1&q2)

    # q1 = "name_contains='过'" if name_like else None
    # q2=",gender=1"
    #
    # Student.objects.filter(eval(q1) if q1 else None)
    # if request.POST:
    #     name_like=request.POST.get('name',None)
    #     gender=request.POST.get('gender',None)
    #     sql = "select * from student"
    #     if request.POST:
    #         sql += "where"
    #         if name_like:
    #             sql += f"name like '%{name_like}%'"      # select * from student where name like "%明%"   (进阶需求)全文搜索
    #         if gender:
    #             sql += f" and gender={gender}"
    #     print(sql)
    #     Student.objects.raw(sql)


    # name_like="明" gender="女"
    # Student.objects.filter().count()

    # 查询
    rows_amount = Student.objects.all().count()
    # page_amount = rows_amount // page_size + 1      # 9条/ 每页3条 整除时导致总页数多算了1。解决方法一 行数-0.1再除；方法二ceil返回大于等于的整数。
    # page_amount = (rows_amount-0.1)//page_size + 1    # [1,2,3]
    page_amount = ceil(rows_amount/page_size)
    page_amount_list = [i for i in range(page_amount)]
    if page_size > page_amount or page_size < 0:
        error_message = '请求页码超过最大页码'

    student_list = Student.objects.all().order_by('no')[start_index: end_index]

    context = {
        'student_list':student_list,
        'page_amount':page_amount,
        'page_amount_list':page_amount_list,
        'page_no':page_no,
        'page_previous':page_no -1,
        'page_next':page_no+1,
    }
    return render(request,'student/index.html',context)

def api_index(request):
    """

    :return:
    '
    {
        "code":200,
        "message":"ok",   # 没有学生数据， 一行都没有
        "count":"80"
        "student_list": [
            {"id":1, "no":"001", "name":"张三", "add_time":"2019-10-09"}
            {"id":1, "no":"001", "name":"张三", "add_time":"2019-10-09"}
        ]
    }
    '
    """

def index2(request):
    pass
    # 用django自带的paginator来实现


def add(request):
    """ 添加表单 """
    # print(request.method)   # GET
    # 有些教程把get和post写到一个视图函数中，通过if request.method == 'GET':
    # 走不同逻辑。但post请求出错时会弹出“表单已提交是否重新加载可能丢失资料的”烦人提示，不利于调试。
    # 所以还是推荐分两个请求来做，一个返回添加页面，一个做存储用户提交数据

    # 获取生成下一个学号
    max_no = Student.objects.aggregate(Max('no'))   # {'no_max':7}
    next_no = max_no['no__max'] + 1
    # select max(id) as amx_id from student_student;
    context = {
        'next_no':next_no,
    }
    return render(request,'student/add.html',context)

def do_add(request):
    """post 存储用户提交的新学生信息"""
    assert request.method == 'POST', 'error: 表单http请求方式应为post'

    # 取参数
    # django框架自带了表单类，先跟model映射好，自动生成表单，自带方法form.isvalid合法性验证 form.save()保存。
    # 但这种方式隐藏了原理，前端不易改css，需要记忆额外的属性来定义表单，在具备前端基础的情况下不推荐使用dj自带的表单
    # 我们这里为了理解原理，前端手写HTML表单，后端存
    args = request.POST
    file = request.FILES  # 文件会存到这个字段里，内存中，open方法打开

    no = args['no']
    name = args['name']
    age = args['age']
    gender = args['gender']
    phone = args['phone']
    avatar = request.FILES.get('avatar')
    # 验证
    # 储存
    student = Student.objects.create(no=no, name=name, age=age, gender=gender, phone=phone,avatar=avatar)
    student.save()
    return render(request, 'student/do_add.html')

def update(request):
    if request.method == 'GET':
        no = request.GET.get('no')
        student = Student.objects.get(no=no)
        context = {
            'student':student
        }
        return render(request,'student/update.html',context)
    if request.method == 'POST':
        id = request.POST.get('id')
        student = Student.objects.get(id=id)
        no = request.POST.get('no')
        name = request.POST.get('name')
        age = request.POST.get('age')
        gender = request.POST.get('gender')
        phone = request.POST.get('phone')
        avatar = request.FILES.get('avatar')
        student.no = no
        student.name = name
        student.age = age
        student.gender = gender
        student.phone = phone
        student.avatar = avatar
        student.save()
        return HttpResponseRedirect( '/student/index/')

def delect(request):
    id = request.GET.get('id')
    delect_student = Student.objects.get(id=id)
    context = {
        'delect_student':delect_student,
    }
    return render(request,'student/delect.html',context)

def do_delect(request):
    no = request.GET.get('no')
    models.Student.objects.get(no=no).delete()
    # return HttpResponseRedirect( '/student/index/')
    return render(request, 'student/do_delect.html')

def query(request):
    if request.method=='GET':
        return render(request,'student/query.html',context={})
    if request.method=='POST':
        name=request.POST.get('name')
        gender = request.POST.get('gender')
        if gender == '未选择':
            gender='0'
        elif gender=='男':
            gender='1'
        elif gender=='女':
            gender='2'
        elif gender=='保密':
            gender='3'

        if name != '' and gender != '':
            stdent_list=Student.objects.filter(name__icontains=name,gender=gender)
        elif name=='' and gender!='':
            student_list=Student.objects.filter(gender=gender)
        elif name!='' and gender=='':
            sutdent_list=Student.objects.filter(name__icontains=name)
        context={
            'student_list':student_list,
        }
        return render(request,'student/query.html',context={})



def export_excel(request):
#     """导出所有学生信息到excel文件"""
#     # 数据库查询学生数据
#     # 数据拼成二维数组(第一行为字段名,后面的数据行(选做)合并两行,填充背景色和修改字体字号)

#     # save(data,afile='media/download/student_info.xlsx')
#     # redriect(to='域名/media/download/student_info.xlsx')
    response = HttpResponse(content_type='application/vnd.ms-excel')
    # response['Content-Disposition'] = 'attachment;filename=student.csv'
    student_stu = Student.objects.all().order_by('no')
    excel_list = [['学号','姓名','年龄','性别','电话']]
    for my in student_stu:
        stu = [my.no,my.name,my.age,my.gender,my.phone]
        excel_list.append(stu)
        save_data(data=excel_list,afile='media/download/stu.csv')
    return response



def cloth_sale_line(request):
    # 后端渲染。 缺点不适合做动态图
    # 获取数据。请求其它接口读数据库
    # 拼前端表格所需的变量
    legend = '销量'
    xAxis = ["衬衫","羊毛衫","雪纺衫","裤子","高跟鞋","袜子"]
    context = {}
    return render('student/8echart.html', context)

def cloth_sale_line_api(request):
    # 前后端分离，前端渲染图表，后端负责返回数据
    # 优点动态图片。缺点js代码复杂。
    legend = '销量'
    xAxis = ["衬衫", "羊毛衫", "雪纺衫", "裤子", "高跟鞋", "袜子"]
    context = {}
    return json.dumps(context)










# select * from student_student limit 0, 3;  -- 学生1-3包含3
# select * from student_student limit 1, 3;   -- 学生2-4
# -- limit 跟python中的列表参数含义不一样, limit 1, 3下标(从0开始计第一行)1, 3表示向后取的行数.
# select * from student_student limit 6, 3;
# -- 计算总行数
# select count(id) as amount from student_student;
#
# page_no 第几页   page_size 一页显示几行    page_amount 总数据个数
# select * from student_student limit 0, {page_size};
# 第1页   每页10条                   0       10
# 第二页                             10      10
#                                    20      10
#                                    start_index = (page_no-1)*page_size
# 总页数    总行除以每页数向上取整   page_amount//10+1     //表示向下取整   //10+1表示向上取整

# student_list = Student.objects.all().order_by('no')[0: 3]
# start_index = (page_no-1) * page_size
# end_index = page_no * page_size



# def do_add(request):
#     """ POST 存储用户提交的新学生信息 """
#     stuClass = Student
#     assert request.method == 'POST', 'error: 表单http请求方式应为post'
#     message = ''
#     error_message = ''
#     # 取参数
#     # dj框架自带了 表单类，先跟model映射好，自动生成表单，自带方法form.isvalid合法性验证  form.save()保存。
#     # 但这种方式隐藏了原理，前端不容易改css，需要记忆额外的属性来自定义表单，在具备前端基础的情况下不推荐使用dj自带的。
#     # 我们这里为了理解原理，前端手写html表单，后端存
#     args = request.POST
#     files = request.FILES
#     user_file = files['avatar']        # 文件会存到这个字段里，类型字典，存放图片的键名为字段名。内存中，后面open方法打开.
#     chunks = user_file.chunks()
#     no = int(args['no'])
#     name = args['name']
#     age = int(args['age'])
#     gender = int(args['gender'])
#     phone = args['phone'] or None
#     _file_name = user_file.name
#     # todo 如果数据库存同名附件 "头像.jpg",但并不意味这内容相同。django会在文件名后自动编号以区分。用hash判断两文件是否相同也可以。
#     _upload_to = Student.avatar.field.upload_to     # 取model中的avatar字段的上传路径，查看ImageField源代码和debug查看Student可发现 # stuClass = Student
#     avatar = _avatar_db_path = os.path.join(_upload_to, _file_name)       # 数据库中路径image/avatar/小米logo_XCOp7og.png
#
#     # 验证
#     # 判断各参数值是否合法。学号是否已存在。等。（实际工作中，挑重要的写，不重要的交给前端表单验证，但后端验证最安全）
#     if no < 0 or no > 10000:
#         error_message = '输入非法，学号范围为 1-9999'
#         # return render()  出现错误返回添加页面，但下面也需要写这行代码重复，明智的做法是判断flag标识，比如error_message是否为空
#     if Student.objects.filter(no=no).exists():
#         max_no = Student.objects.aggregate(Max('no'))['max__no']
#         error_message = f'学号已存在, 目前最大学号为{max_no},建议学号设置为{max_no+1}.'
#     if gender not in [i[0] for i in Student.GENDER_CHOICES]:
#         error_message = '性别可选值不正确'
#
#     # 存储信息
#     try:
#         stu = Student(no=no,
#                       name=name,
#                       age=age,
#                       gender=gender,
#                       phone=phone,
#                       avatar=avatar)
#         stu.save()
#         message = '数据库存储完毕。'
#     except Exception as e:
#         error_message += '数据库执行错误。'
#
#     # 存储文件
#     try:
#         _avatar_abs_path = os.path.join(settings.MEDIA_ROOT, _avatar_db_path)       #  D:/project/media/image/avatar/xxx.jpg
#         with open(file=_avatar_abs_path, mode='wb') as file:        # 写二进制，不熟悉的先看https://code.aliyun.com/zzdxyz/tutorial/tree/master/L7%E6%9C%AC%E5%9C%B0%E6%96%87%E4%BB%B6%E8%AF%BB%E5%86%99
#             for chunk in user_file.chunks():        # user_file.chunks()获取客户端传来的二进制分块列表  b'\x02\x33\...'
#                 file.write(chunk)
#             message += '附件存储完毕。'        # 这时media文件夹下就有图片了，pycharm有时过几秒才能看到目录更新
#     except Exception as e:
#         error_message += '本地存储文件错误 路径错误或没有权限。'
#
#     context = {
#         'message': message,
#         'error_message': error_message,
#     }
#
#     if error_message:
#         return render(request, 'student/add.html', context)
#     else:
#         # 运行正确
#         return render(request, 'student/success.html', context)
