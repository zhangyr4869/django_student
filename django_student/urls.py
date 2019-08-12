"""django_student URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
# from . import settings 不建议通过python包方式导入，django加载变量和代码存在顺序，直接导入settings可能导致报错。
# 而是导入源代码的settings，它会在合适的时候导入变量。
from django.conf import settings
from django.conf.urls.static import static
from django.views.static import serve



urlpatterns = [
    path('admin/', admin.site.urls),
    # 127.0.0.1:8000/student/*
    path('student/', include('student.urls')),
    path('login/', include('login.urls')),


    # from student import views
    # http://127.0.0.1:8000
    # path('',views.index)
    # http://127.0.0.1:8000/index
    # path('',views.index)

    # static('^media\/(?p<path>.*)$', document_root=settings.MEDIA_ROOT)
    # static(settings.MEDIA_URL, serve, {'document_root=settings.MEDIA_ROOT})



]
# static ( '客户端请求的url /media',  电脑本地的file文件夹)
# static 函数返回 [rpath('media','d:project/media')]
# urlpatterns = urlpatterns + static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
# http://127.0.0.1:8000/media/image/avatar/1.jpg
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


