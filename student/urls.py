from django.urls import path

from .import views

urlpatterns = [
    path('index/',views.index,name='index'),
    path('add/',views.add,name='add'),
    path('do_add/',views.do_add,name='do_add'),
    path('update/',views.update,name='update'),
    path('delect/',views.delect,name='delect'),
    path('do_delect/',views.do_delect,name='do_delect'),

    path('export_excel/',views.export_excel,name='export_excel'),
    path('query/',views.query,name='query'),

    path('api/index/',views.index,name='index'),     # /student/api/index
]



# 大多数情况两种方式可互换
#方式一:如果参数1个,且与业务关系较大,适合动态url匹配方式,   bill.com/av/58888/  path(av/<av_id>)    视图函数的参数获取到
# 方式二:参数较多,适合query string , url后?传参
# bill.com/news/?page_no=2&page_size=20 , path('news/') ,视图函数中requestGET['page_no']