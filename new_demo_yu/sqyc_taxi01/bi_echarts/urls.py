from django.conf.urls import include, url
from django.contrib import admin
from bi_echarts import  views


urlpatterns = [
    # url(r'show_map/$',views.demo_bi_echarts),
    url(r'map/$', views.Order_map_data),
    url(r'func_add/$',views.Func_add),
]