from django.shortcuts import render
from django.http import  HttpResponse
from django.views.decorators.http import  require_POST,require_GET,require_http_methods
from sqyc_bi.models import *
from django.http import HttpResponseNotAllowed,JsonResponse

import csv
from sqyc_bi.models import  *
# Create your views here.
from sqyc_bi.untils.decorators import *
from sqyc_bi.untils.down_func import  *
from  sqyc_bi.untils.rtn_pages import  *
from django.core.paginator import Paginator
import  pymysql

from django.db import  connection


def Index(request):
    #return  HttpResponse('欢迎来到首约科技事业部BI报表')

    return render(request, 'sqyc_bi/login_index_new.html')



@require_http_methods(['GET','POST'])
def User_account01(request):
    '''显示注册页面'''
    if request.method=='GET':
        return render(request,'sqyc_bi/user_admin.html')
    elif request.method=='POST':
        user_name = request.POST.get('uname')
        password = request.POST.get('passwd')
        adminpasswd = request.POST.get('adminpasswd')

        user_account.objects.add_one_manager(user_name, password, adminpasswd)
        return  HttpResponse("ok!")



@require_http_methods(['GET','POST'])
def User_account(request):
    '''管理注册页面'''
    if request.method == 'GET':
        return render(request, 'sqyc_bi/user_admin.html')
    elif request.method=='POST':
        user_model = user_account()
        user_model.user_name = request.POST.get('uname')
        user_model.password = get_hash( request.POST.get('passwd') )
        user_model.adminpasswd = request.POST.get('adminpasswd')
        if user_model.adminpasswd == "helloworld":
            user_model.save()
            return HttpResponse("注册ok！"   )
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
    # login_model = user_account()  # user_account 模型类
    # the_data = login_model.objects.filter(user_name=username, password=pwd)
    the_data = user_account.objects.filter(user_name= username, password = get_hash(pwd) )
    # return JsonResponse( {'res':the_data} )

    if   the_data :
        # 3 返回授权页面
        request.session['is_login'] = True
        request.session['user_name'] = username
        # request.session['user_id'] = the_data.id

        if username in ['nihao', 'sqyc_admin']:
            privileges = 'normal'
        else :
            privileges = 'hid'

        return render(request, 'sqyc_bi/base_in_index.html', {"privileges":privileges })

    else:

        # the_data = 'haha%s' %the_data
        # return HttpResponse(the_data)
        return HttpResponse("账户或者密码错误！")



@login_required
def Wd_driver_num(request,page_index):
    ''' 返回接单员数量信息，日期， 订单状态， 有无拉新；  一单，二单'''

    recmd_status = request.GET.get('recmd_status')
    pro_status = request.GET.get('pro_status')
    # t_date = request.GET.get('t_date')
    sub_buton = request.GET.get('sub_buton')

    if sub_buton =="下载所有数据":
        order_list = t_driver_order_num.objects.all()
        order_list = Down_files(request, order_list, create_date ='日期', order_status='订单状态', one_num='一单' )
        return  order_list
    else:
        order_list = t_driver_order_num.objects.filter( order_status=pro_status)

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
        #总页数小于等于5
        pages = range(1,num_pages+1)
    elif current_num <=5:
        # 当前页为前5页
        pages = range(1,11)
    elif num_pages - current_num<=4:
        # 當前頁爲後5頁
        pages = range(num_pages-10, num_pages+1)
    else:
        # 既不是前5页，也不是后5页
        pages = range(current_num-5, current_num+5)

    # 返回数据
    return  render(request, 'sqyc_bi/base_in_order_num.html', {'order_list':order_list,
                                                               'pages':pages ,
                                                               'recmd_status':recmd_status,
                                                               'pro_status':pro_status,
                                                               # 't_d':t_date
                                                               })


@login_required
def Company_first(request):
    return render(request,'sqyc_bi/base_in_company_day.html')



@login_required
def Company_day(request,page_index):
    ''' 日报 ： com_cnt, reward_punish_money, total_online_minute'''
    city_id = request.GET.get('para1')
    company_name = request.GET.get('para2')
    t_d = request.GET.get('t_d')

    sub_buton = request.GET.get('sub_buton')


    if sub_buton == '下载所有数据':


        company_list = t_company_day_data.objects.filter(city_id=city_id,
                                                         taxi_company_name__regex=company_name, t_date=t_d)

        company_list = Down_files(request, company_list, t_date='日期', city='city', driver_id='driver_id',
                                  driver_name='driver_name',driver_phone='driver_phone', taxi_company_name='公司',
                                  com_cnt='完单量', plate_number='车牌号', id_number='证件号',total_online_minute='在线分钟')
        return  company_list
    else:
        company_list = t_company_day_data.objects.filter(city_id=city_id, taxi_company_name__regex=company_name, t_date=t_d)

    order_list, pages = Rtn_pages(company_list, page_index)


    return  render(request,'sqyc_bi/base_in_company_day.html',
                   {'order_list':order_list,
                    'pages':pages,
                    'city_id':city_id ,
                    'company_name':company_name,
                    't_d':t_d } )


@login_required
def Company_day_total_first(request):
    return render(request, 'sqyc_bi/company_day_total.html')


@login_required
#  sq_yunying , sq_sj  ,  taxi_beijing_44,  taxi_haerbin_94
def Company_day_total(request, page_index):
    '''公司汇总数据 公司， 证件  车牌 在线分钟 完单量 在线天数'''
    t_d1 = request.GET.get('t_d1')
    t_d2 = request.GET.get('t_d2')
    city_id = request.GET.get('para1')
    company_name = request.GET.get('para2')
    sub_buton = request.GET.get('sub_buton')


    cur = connection.cursor()
    if (company_name in ("大众", "天鹅") ) and sub_buton =="下载数据":
        cur = connection.cursor()
        sql = "SELECT * from  t_special_company_day('%s','%s','%s')"  %(t_d1, t_d2, company_name)
    else:
        sql = "select * from fuc_company_total('%s','%s', '%s','%s')" % (company_name, t_d1, t_d2, city_id)
        # sql = "call fuc_company_total('%s','%s', '%s','%s')" %(company_name,t_d1, t_d2,city_id)


    cur.execute(sql)
    res = cur.fetchall()
    # 处理方式二， 形成字典列表
    colName = [col[0] for col in cur.description]
    order_list = [dict(zip(colName, row)) for row in res]  # 将字典及数据用列表推导式定 === 列表推导式

    # order_list = []
    # for i in res:
    #     dic = {}
    #     dic['taxi_company_name'] = i[0]
    #     dic['id_number'] = i[1]
    #     dic['plate_number'] = i[2]
    #     dic['driver_name'] = i[3]
    #
    #     dic['sum_online_minute'] = i[4]
    #     dic['sum_com_cnt'] = i[5]
    #     dic['online_day'] = i[6]
    #     order_list.append(dic)


    if sub_buton =="下载数据":
        order_list = Down_files_dic2(request, order_list, colName)
        return order_list
        #
        # order_list = Down_files_dic(request, order_list, taxi_company_name='公司名称',id_number= '证件号',
        #                             plate_number = "车牌号", driver_name = '司机姓名', sum_online_minute ='在线分钟',  sum_com_cnt ='完单数'
        #                             , online_day ='在线天数' )
        return order_list
    else:
        order_list , pages = Rtn_pages(order_list, page_index)


    return  render(request, 'sqyc_bi/company_day_total.html', {'order_list':order_list,'company_name':company_name,
                                                               'pages':pages,'t_d1':t_d1,
                                                               't_d2':t_d2 ,
                                                               'city_id':city_id } )


@login_required
def t_s_company_first(request):
    '''test 初始化测试'''
    return  render(request, "sqyc_bi/fun_city_total.html")

@login_required
def t_s_company(request,page_index):
    # 阶段汇总数据:  单位名称  司机数 上线司机数	未上线司机数	上线率 完单数	完单司机数 , todo

    city_id = request.GET.get('para1')
    t_d1 = request.GET.get('t_d1')
    t_d2 = request.GET.get('t_d2')
    sub_buton = request.GET.get('sub_buton')

    cur = connection.cursor()
    sql = "select * from  fuc_city_total('%s','%s', '%s' )" %(t_d1, t_d2,city_id)
    cur.execute(sql)
    res = cur.fetchall()

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

    if sub_buton =="下载数据":
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


    return   render(request, 'sqyc_bi/fun_city_total.html', {'order_list':order_list, 'pages':pages ,
                                                             'city_id':city_id, 't_d1':t_d1, 't_d2':t_d2})

    pass



def Auto_list(request):
    return render(request, 'sqyc_bi/auto_index.html')



def Handle_sql(request):
    return render(request, 'bi_echarts/Handle_sql.html')

    pass

def Handle_sqlt(request):
    sub_buton = request.GET.get('sub_buton')
    para1 = request.GET.get('para1')

    cur = connection.cursor()

    sql = para1.strip().replace(r"\n","")
    cur.execute(sql)
    res = cur.fetchall()

    colName = [col[0] for col in cur.description]
    order_list = [dict(zip(colName, row)) for row in res]
    order_list = Down_files_dic2( request, order_list, colName)
    return  order_list



@login_required
def Other_test(request):
    str = "本功能暂未开发！"
    return  HttpResponse(str)




# def Other_test(request):
#
#     return  render(request, 'sqyc_bi/fun_city_total.html')
#

def company_test(request):
    cur = connection.cursor()
    sql = "call fuc_city_total('2018-05-20', '2018-05-22', 94) "
    cur.execute(sql)
    res = cur.fetchall()

    order_list = []
    for i in res:
        dic = {}
        dic['taxi_company_name'] = i[0]
        dic['driver_cnt'] = i[1]
        dic['com_order_cnt'] = i[2]

        order_list.append(dic)

    return JsonResponse( {"name":"yusir","age":20, "address":"beijing"} )
    # return  JsonResponse(order_list)



@login_required
def Sqmap(request):

    return render(request, 'sqyc_bi/sqmap.html')


@login_required
def Connect(request):

    return  HttpResponse('问题联系方式： yuweihong@01zhuanche.com')

@login_required
def Passenger_check(request):

    return render(request, 'sqyc_bi/passenger_check.html')


@login_required
def Driver_check(request):

    return   HttpResponse("本功能待开发， 敬请期待 ！！")

@login_required
def Else_check(request):

    return   HttpResponse("本功能待开发， 敬请期待 ！！")







