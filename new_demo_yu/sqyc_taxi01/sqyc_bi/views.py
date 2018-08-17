from django.shortcuts import render
from django.http import  HttpResponse
from django.views.decorators.http import  require_POST,require_GET,require_http_methods
from sqyc_bi.models import *
from django.http import HttpResponseNotAllowed,JsonResponse

import csv
from bi_echarts.models import  *
# Create your views here.
from sqyc_bi.untils.decorators import *
from sqyc_bi.untils.down_func import  *
from  sqyc_bi.untils.rtn_pages import  *
from django.core.paginator import Paginator
import  pymysql

from django.db import  connection
from sqyc_bi.data_tools import  *
import datetime
from multiprocessing import Process
import time

def Index(request):
    #return  HttpResponse('欢迎来到首约科技事业部BI报表')
    return render(request, 'sqyc_bi/login_index_new.html')


#
# @require_http_methods(['GET','POST'])
# def User_account01(request):
#     '''显示注册页面'''
#     if request.method=='GET':
#         return render(request,'sqyc_bi/user_admin.html')
#     elif request.method=='POST':
#         user_name = request.POST.get('uname')
#         password = request.POST.get('passwd')
#         adminpasswd = request.POST.get('adminpasswd')
#         user_account.objects.add_one_manager(user_name, password, adminpasswd )
#     return  HttpResponse("ok!")


@require_http_methods(['GET','POST'])
def User_account(request):
    '''管理注册页面'''
    if request.method == 'GET':
        return render(request, 'sqyc_bi/user_admin.html')
    elif request.method == 'POST':
        user_model = user_account()
        user_model.user_name = request.POST.get('uname')
        user_model.password = get_hash( request.POST.get('passwd') )
        user_model.adminpasswd = request.POST.get('adminpasswd')
        if user_model.adminpasswd == "helloworld":
            user_model.save()
            return HttpResponse("恭喜！注册成功！")
        else:
            str1= "暗号错误,注册失败！%s" %user_model.adminpasswd
            return HttpResponse(str1 )


@require_http_methods(['GET','POST'])
def Login_check(request):
    '''用户登录检查'''
    # 1 获取用户
    username = request.POST.get('username')
    pwd = request.POST.get('pwd')

    # 2 检查核对
    the_data = user_account.objects.filter(user_name= username, password = get_hash(pwd) )
    # return JsonResponse( {'res':the_data} )

    if   the_data :
        # 3 返回授权页面
        request.session['is_login'] = True
        request.session['user_name'] = username
        privileges = user_account.objects.get(user_name = username, password = get_hash(pwd) )
        request.session['privileges'] = privileges.comment

        # REC : name ,comment, -- date
        rec_model = t_rec_table()
        rec_model.the_name = username
        rec_model.comment = 'login'
        rec_model.save()

        # if username in ['nihao', 'sqyc_admin']:
        #     privileges = 'normal'
        # else :
        #     privileges = 'hid'
        return render(request, 'sqyc_bi/base_in_index.html', {"privileges":privileges.comment })
    else:
        return HttpResponse("账户或者密码错误！")



@login_required
def Wd_driver_num_fr(request):
    '''测试'''
    return render(request, 'sqyc_bi/base_in_order_num.html')


@require_http_methods(['GET','POST'])
@login_required
def Wd_driver_num(request,page_index):
    ''' 返回接单员数量信息,日期, 订单状态, 有无拉新；  一单,二单  bug_todolist'''
    recmd_status = request.GET.get('recmd_status')
    pro_status = request.GET.get('pro_status')
    # t_date = request.POST.get('t_date')
    sub_buton = request.GET.get('sub_buton')
    if sub_buton =="下载所有数据":
        order_list = t_driver_order_num.objects.all()
        order_list = Down_files(request, order_list, create_date ='日期', order_status='订单状态', one_num='一单' )
        return order_list
    else:
        order_list = t_driver_order_num.objects.filter( order_status=pro_status).order_by('-create_date')

    # 1进行分页
    paginator = Paginator(order_list,20)
    # 2获取第n页内容
    order_list = paginator.page(int(page_index))
    # 3获取页码列表
    pages = paginator.page_range
    # 4.1获取总页数
    num_pages = paginator.num_pages
    current_num = int(page_index)

    if num_pages<=10:
        pages = range(1,num_pages+1)  #总页数小于等于5
    elif current_num <=5:
        pages = range(1,11)    # 当前页为前5页
    elif num_pages - current_num<=4:
        pages = range(num_pages-10, num_pages+1)  # 當前頁爲後5頁
    else:
        pages = range(current_num-5, current_num+5)   # 既不是前5页，也不是后5页
    # 返回数据
    return  render(request, 'sqyc_bi/base_in_order_num.html', {'order_list':order_list,
                                                               'pages':pages ,
                                                               'recmd_status':recmd_status,
                                                               'pro_status':pro_status, })

@login_required
def Company_day_fr(request):
    '''fr company_day test '''
    return render(request, 'sqyc_bi/base_in_company_day.html')


@login_required
def Company_day(request,page_index):
    ''' 日报 ： com_cnt, reward_punish_money, total_online_minute'''
    city_id = request.GET.get('para1')
    company_name = request.GET.get('para2')
    t_d = request.GET.get('t_d')

    if request.session['user_name'].split("_")[0] == 'sqtaxi':
        city_id = request.session['user_name'].split("_")[-1]

    sub_buton = request.GET.get('sub_buton')
    if sub_buton == '下载所有数据':
        company_list = t_company_day_data.objects.filter(city_id=city_id,
                                                         taxi_company_name__regex=company_name, t_date=t_d)
        company_list = Down_files(request, company_list, t_date='日期', city='city', driver_id='driver_id',
                                  driver_name='driver_name',driver_phone='driver_phone', taxi_company_name='公司',
                                  com_cnt='完单量', plate_number='车牌号', id_number='证件号',total_online_minute='在线分钟')
        return company_list
    else:
        company_list = t_company_day_data.objects.filter(city_id=city_id, taxi_company_name__regex=company_name, t_date=t_d)
    #   分页函数
    order_list, pages = Rtn_pages(company_list, page_index)

    return  render(request, 'sqyc_bi/base_in_company_day.html', {'order_list': order_list,'pages': pages, 'city_id': city_id,
                    'company_name': company_name,'t_d': t_d})


def Company_day_total_fr(request):
    return render(request, 'sqyc_bi/company_day_total.html')


@login_required
def Company_day_total(request, page_index):
    '''公司汇总数据 公司 证件 车牌 在线分钟 完单量 在线天数 ,  sqtaxi_beijing_44,  sqtaxi_haerbin_94,'''
    t_d1 = request.GET.get('t_d1')
    t_d2 = request.GET.get('t_d2')
    city_id = request.GET.get('para1')
    if request.session['user_name'].split("_")[0] == 'sqtaxi':
        city_id = request.session['user_name'].split("_")[-1]
    company_name = request.GET.get('para2')
    sub_buton = request.GET.get('sub_buton')

    # 大众， 天鹅特殊情况， 额外处理
    if (company_name in ("大众", "天鹅") ) and sub_buton =="下载数据":
        # Pg数据库存储过程大的使用方式， 与mysql略不同
        sql = "SELECT * from  t_special_company_day('%s','%s','%s')"  %(t_d1, t_d2, company_name)
    else:
        sql = "select * from fuc_company_total('%s','%s', '%s','%s')" % (company_name, t_d1, t_d2, city_id)

    cur = connection.cursor()
    cur.execute(sql)
    res = cur.fetchall()

    # 处理方式2 列表推导式~ (分公司透视用的处理方式一-- 字典形式组成)
    colName = [col[0] for col in cur.description]  # 列名
    order_list = [dict(zip(colName, row)) for row in res]  # 列名&行绑定， 处理为字典对象

    if sub_buton =="下载数据":
        order_list = Down_files_dic2(request, order_list, colName)
        return order_list
    else:
        # 分页
        order_list , pages = Rtn_pages(order_list, page_index)
    return render(request, 'sqyc_bi/company_day_total.html', {'order_list': order_list,
                                                               'company_name': company_name,
                                                               'pages': pages,
                                                               't_d1': t_d1,
                                                               't_d2': t_d2 ,
                                                               'city_id': city_id } )


@login_required
def t_s_company_first(request):
    ''' 测试用 '''
    return render(request, "sqyc_bi/fun_city_total.html")


@login_required
def t_s_company(request,page_index):
    # city阶段汇总数据:单位名称-司机数-上线司机数-完单数-完单司机数 , todolist
    city_id = request.GET.get('para1')
    if request.session['user_name'].split("_")[0] == 'sqtaxi':
        city_id = request.session['user_name'].split("_")[-1]
    t_d1 = request.GET.get('t_d1')
    t_d2 = request.GET.get('t_d2')
    sub_btn = request.GET.get('sub_buton')

    cur = connection.cursor()
    sql = "select * from  fuc_city_total('%s','%s', '%s' )" %(t_d1, t_d2,city_id)
    cur.execute(sql)
    res = cur.fetchall()

    # 处理方式1 普通字典形式;  方式2 列表推导式 cur.description 方法
    order_list = []
    for i in res:
        dic ={}
        dic['taxi_company_id'] = i[0]
        dic['taxi_company_name'] = i[1]
        dic['driver_cnt'] = i[2]
        dic['com_order_cnt'] = i[3]
        dic['com_driver_cnt'] = i[4]
        dic['online_driver_cnt'] = i[5]
        order_list.append(dic)

    if sub_btn =="下载数据":
        order_list = Down_files_dic(request, order_list,
                                    taxi_company_id = 'company_id',
                                    taxi_company_name='公司名称',
                                    driver_cnt='司机数量',
                                    com_order_cnt='完单数量',
                                    com_driver_cnt='完单司机数',
                                    online_driver_cnt='登录司机数')
        return order_list
    else:
        order_list , pages = Rtn_pages(order_list, page_index)
    return render(request, 'sqyc_bi/fun_city_total.html', {'order_list':order_list, 'ages':pages, 'city_id':city_id, 't_d1':t_d1,'t_d2':t_d2})



@login_required
def Other_test(request):
    str = "您好！本功能待开发！"
    return  HttpResponse(str)


@login_required
def Connect(request):
    return  HttpResponse('问题联系方式： YuWeihong')

    
@login_required
def Handle_sqlt(request):
    if request.method == 'GET':
        order_list = func_comment.objects.all()
        # order_list, pages = Rtn_pages(order_list, page_index)
        return render(request, 'bi_echarts/Handle_sql.html', {'order_list': order_list})
    elif request.method == 'POST':
        to_add = request.POST.get('recevi_person')
        par_name = request.POST.get('par_name')
        sql = request.POST.get('para1').strip().replace(r"\n"," ")

        #  REC,  thename-- sql-- date-- other
        rec_model = t_rec_table()
        rec_model.the_name = request.session.get('user_name')
        rec_model.comment = sql
        rec_model.save()

        pro = Process(target=mail_mimemuprt_n, args=(sql,par_name,to_add,) ) # 发邮件的那个函数接口
        pro.start()
        time.sleep(0.2)
        return HttpResponse("<h2>您的需求已添加任务,请稍后查收邮件!</h2> <h3>(网络>>服务器>>数据量>>均会影响任务进度,请了解!)</h3>")


def Handle_del(request, theid):
    ''' 删除添加备注里的信息 '''
    order_list = func_comment.objects.filter(id = theid)
    order_list.delete()
    return  redirect('/handle_sqlt/')


@login_required
def Look_reward(request):
    if request.method == 'GET':
        return  render(request, 'sqyc_bi/look_reward.html')
    elif request.method == 'POST':
        prm_phone = request.POST.get('prm_phone')
        prm_city = request.POST.get('prm_city')
        prm_date = request.POST.get('prm_date')
        sql = "SELECT driver_id from mysql.taxi_account_driver where driver_phone = '{}'".format(prm_phone)
        cur = connection.cursor()
        cur.execute(sql)
        res = cur.fetchall()

        # driver_id,  city_id, tdate
        sql2 = "SELECT * from func_dr_rec_chk('{}', {}, '{}')".format(res[0][0],prm_city,prm_date )
        cur.execute(sql2)
        res2 = cur.fetchall()

        colname = [col[0] for col in cur.description ]
        order_list = [dict(zip(colname ,row)) for row in res2 ]
        # return  HttpResponse(colname)
        return render(request, 'sqyc_bi/look_reward.html',  {'order_list':order_list,'prm_phone':prm_phone,
                                                             'prm_city':prm_city,'prm_date':prm_date } )


@login_required
def Auto_check(request):
    cur = connection.cursor()
    if request.method == 'GET':
        return render(request, 'sqyc_bi/auto_index.html')
    elif request.method == 'POST':
        par_custid = request.POST.get("par_custid")
        sql = "select 司机id dr_id, 司机姓名 dr_name, 司机身份证 dr_cid,  city_id ctyid, 城市 city, 司机手机号 dr_phone, 出租车公司 taxi_company,  司机端状态 app_status, 司机钱包状态 p_status \
  from public.who_are_you( '{}') ".format(par_custid)
        cur.execute(sql)
        res = cur.fetchall()

        colname = [col[0] for col in cur.description]
        order_list = [ dict(zip(colname, row)) for row in res]
        return render(request, 'sqyc_bi/auto_index.html', {'order_list':order_list,'cust_id':par_custid})


def Cust_id_random(request):
    par_custid = request.POST.get('par_custid')
    par_sl = request.POST.get('par_sl')
    cur = connection.cursor()
    if par_sl == "生成":
        sql = "select  * from random_china_id('999',v_date=>'O')"
    elif par_sl == "验证":
        sql = "select * from check_china_id('{}')".format(par_custid)

    cur.execute(sql)
    res = cur.fetchall()
    colname = [col[0] for col in cur.description]
    order_list = [dict(zip(colname, row)) for row in res]

    return render(request, 'sqyc_bi/auto_index.html', {'order_list':order_list})





















