from django.shortcuts import redirect
from django.http import  HttpResponse
from sqyc_bi.models import  *


def login_required(view_func):
    ''' 用户登录判断装饰器'''
    def wrapper(request, *args, **kwargs):
        if request.session.has_key('is_login'):
            # 用户登录
            return  view_func(request, *args, **kwargs)
        else:
            # 用户没登录,跳转到登录页面
            return HttpResponse("您好！请检查是否登录！")
    return wrapper




