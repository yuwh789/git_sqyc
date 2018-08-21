from django.conf.urls import include, url
from django.contrib import admin
from bi_echarts import  views


urlpatterns = [
    url(r'show_map/$',views.Order_map_data),
    url(r'map/$', views.Order_map_data),
    url(r'func_add/$',views.Func_add),
]