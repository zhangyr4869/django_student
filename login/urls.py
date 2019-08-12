from django.urls import path
from . import views

urlpatterns = [
    path('index/',views.index),
    path('register/',views.register),
    path('register_check/',views.register_check),
    path('do_register/',views.do_register),
    path('login/',views.login),
    path('do_login/',views.do_login),
    path('logout/',views.logout),
    # path('register_email_active/',views.register_email_active),
]