from django.conf.urls import include, url
from django.contrib import admin
from sqyc_bi import  views

urlpatterns = [
    url(r'^$', views.Index) ,
    url(r'^inner_index/$', views.Login_check ) ,

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
    url(r'^company_day/(\d+)/$', views.Company_day),

    url(r'^company_day_total/$', views.Company_day_total_first) , # 页面 分公司汇总初始

    url(r'^company_day_total/(\d+)/$', views.Company_day_total) ,

    url(r'^company_test/$', views.company_test),
    url(r"^city_total/$",views.t_s_company_first), # 城市各分公司数据 初始化测试
    url(r"city_total/(\d+)/$", views.t_s_company)  ,

    url(r"^auto_list/$", views.Auto_list) ,

    url(r'^handle_sql/$', views.Handle_sql) ,
    url(r'^handle_sqlt/$', views.Handle_sqlt)
    # url(r"^special_com_total/$", views.Special_com_total) ,

]