# Create your views here.
from django.shortcuts import render
from django.http import  HttpResponse
from django.db import  connection
# Create your views here.
from sqyc_bi.untils.decorators import *

# from django.contrib.auth.decorators import login_required


@login_required
def demo_bi_echarts(request):

    return  render(request, 'bi_echarts/order_hot_map.html')



@login_required
def Order_map_data(request):
    t_city = request.GET.get("t_city")
    t_d1 = request.GET.get("t_d1")
    t_d2 = request.GET.get("t_d2")
    check = request.GET.get("ck")

    cur = connection.cursor()
    # sql = "select * from order_lat_long where  city_id={}".format()

    sql = "SELECT * from order_lat_long('{}','{}' ,'{}') ".format(t_d1,t_d2,t_city)

    cur.execute(sql)
    res = cur.fetchall()

    order_list = []
    for i in res:
        dic = {}
        # dic['city_id'] = i[0]
        dic['lng'] = i[0].split(",")[0]
        dic['lat'] = i[0].split(",")[-1]
        dic['count'] = i[1]

        order_list.append(dic)

    if check == "ck2":
        return  HttpResponse("可选库")

    return  render(request, 'bi_echarts/order_hot_map.html',  {'order_list':order_list ,
                                                               't_city':t_city,
                                                               't_d1':t_d1,
                                                               't_d2':t_d2} )

