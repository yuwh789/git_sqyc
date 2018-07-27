# Create your views here.
from django.shortcuts import render
from django.http import  HttpResponse
from django.db import  connection
# Create your views here.
from sqyc_bi.untils.decorators import *
from bi_echarts import  models

from django.shortcuts import redirect
# from django.contrib.auth.decorators import login_required


# @login_required
# def demo_bi_echarts(request):
#
#     return  render(request, 'bi_echarts/order_hot_map.html')



@login_required
def Order_map_data(request):
    if request.method == "GET":
        return render(request, 'bi_echarts/order_hot_map.html')
    elif request.method == "POST":
        t_city = request.POST.get("t_city")
        t_d1 = request.POST.get("t_d1")
        t_d2 = request.POST.get("t_d2")
        check = request.POST.get("ck")

        cur = connection.cursor()
        # Pg数据库存储过程用法， 与mysql略有差异
        sql = "SELECT * from order_lat_long('{}','{}' ,'{}') ".format(t_d1, t_d2, t_city)
        # 测试库判断
        if check == "ck2":
            sql = "SELECT * from order_lat_long_test('{}','{}' ,'{}') ".format(t_d1, t_d2, t_city)
        cur.execute(sql)
        res = cur.fetchall()

        order_list = []
        for i in res:
            '''i tuple'''
            dic = {}
            dic['lng'] = i[0].split(",")[0]
            dic['lat'] = i[0].split(",")[-1]
            dic['count'] = i[1]
            order_list.append(dic)
        return  render(request, 'bi_echarts/order_hot_map.html',
                       {'order_list':order_list, 't_city':t_city, 't_d1':t_d1, 't_d2':t_d2})


# @login_required
def Func_add(request):
    if request.method == 'GET':
        return render(request, 'bi_echarts/func_add.html', )
    elif request.method == 'POST':
        func_model = models.func_comment()
        func_model.title = request.POST.get('para1')
        func_model.func_name = request.POST.get('para2')
        func_model.comment = request.POST.get('para3')
        func_model.save()
        return redirect('/handle_sqlt/')

    pass
