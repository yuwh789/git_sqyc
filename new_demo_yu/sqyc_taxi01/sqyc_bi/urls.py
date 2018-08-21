from django.conf.urls import include, url
from django.contrib import admin
from sqyc_bi import  views

urlpatterns = [
    url(r'^$', views.Index) ,
    url(r'^inner_index/$', views.Login_check ) ,
    url(r'^user_account/$',views.User_account) , # user_account

    url(r'^order_driver_num_fr/$', views.Wd_driver_num_fr),
    url(r'^order_driver_num/(\d+)/$',views.Wd_driver_num),

    url(r'^Company_day_fr/$', views.Company_day_fr),
    url(r'^company_day/(\d+)/$', views.Company_day), # every_day data

    url(r'^company_day_total_fr/$', views.Company_day_total_fr),
    url(r'^company_day_total/(\d+)/$', views.Company_day_total) , #  by stages--company data

    url(r'^other/test/$', views.Other_test),  # 测试 Todo
    # url(r'^sqmap/$',views.Sqmap ), # baidu地图>>迁移到chart url里
    url(r'^connect/$',views.Connect ) , # my_connect

    url(r"^city_total/$",views.t_s_company_first), # 城市各分公司数据 初始化测试
    url(r"city_total/(\d+)/$", views.t_s_company), # 阶段city data

    url(r'^handle_sqlt/$', views.Handle_sqlt),
    # url(r"^special_com_total/$", views.Special_com_total) ,
    url(r'^handle_del/(\d+)/$', views.Handle_del) ,

    url(r'^look_reward/$', views.Look_reward),
    url(r"^auto_check/$", views.Auto_check) ,

    url(r'cust_id_random/$', views.Cust_id_random),

]