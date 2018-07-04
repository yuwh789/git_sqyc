from django.conf.urls import include, url
from django.contrib import admin
from sqyc_bi import  views

urlpatterns = [
    url(r'^$', views.Index) ,
    url(r'^inner_index/$', views.Login_check ) ,
    url(r'^csv/$', views.Csv_data ) , # download something

    url(r'^sqmap/$',views.Sqmap ),
    url(r'^connect/$',views.Connect ) ,
    url(r'^passenger_check/$', views.Passenger_check),

    url(r'^driver_check/$', views.Driver_check ) ,
    url(r'^else_check/$', views.Else_check),   # else_check
    # url(r'^sqyc_index/', views.Sqyc_index),  # sqyc_index

    url(r'^user_account/$',views.User_account) , # user_account

    url(r'^order_driver_num/(\d+)/$',views.Wd_driver_num),

    url(r'^other/test/$', views.Other_test) ,  # 测试
    # url(r'^pas/exper/$', views.Pas_exper)   # 乘客体验
    url(r'^company_day/$', views.Company_first) ,
    url(r'^company_day/(\d+)/$', views.Company_day)
]