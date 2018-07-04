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
        return render(request, 'sqyc_bi/base_in_index.html')

    else:

        # the_data = 'haha%s' %the_data
        # return HttpResponse(the_data)
        return HttpResponse("账户或者密码错误！")



@login_required
def Csv_data(request):
    # Create the HttpResponse object with the appropriate CSV header.
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="download_files.csv"'

    writer = csv.writer(response)
    # 取出城市代码， 依据命名格式。
    the_name = request.session['user_name'].split("_")[-1]
    writer.writerow([the_name])
    data_list = sqyc_table.objects.all()[0:30]

    writer.writerow(['city_id',  'driver_id', 'driver_phone' ])
    for i in data_list:
        writer.writerow( [i.city_id,  i.driver_id, i.driver_phone]  )

    return response



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
        order_list = t_driver_order_num.objects.filter(order_status=pro_status).order_by('-create_date')

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


# def Pas_exper(request,page_index):
#
#
#     pass
@login_required
def Company_first(request):
    return render(request,'sqyc_bi/base_in_company_day.html')


@login_required
def Company_day(request,page_index):
    city_id = request.GET.get('para1')
    company_name = request.GET.get('para2')
    t_d = request.GET.get('t_d')

    sub_buton = request.GET.get('sub_buton')

    if sub_buton == '下载所有数据':
        company_list = t_company_day_data.objects.filter(city_id=city_id, taxi_company_name__regex=company_name,
                                                         t_date=t_d)
        company_list = Down_files(request, company_list, t_date='日期', city='city', driver_id='driver_id',
                                  driver_name='driver_name',
                                  driver_phone='driver_phone', taxi_company_name='公司', com_cnt='完单量',
                                  plate_number='车牌号', id_number='证件号',
                                  total_online_minute='在线分钟')
        return  company_list


    else:
        company_list = t_company_day_data.objects.filter(city_id=city_id, taxi_company_name__regex=company_name, t_date=t_d)


    # 1进行分页
    paginator = Paginator(company_list, 20)

    # 2获取第n页内容
    company_list = paginator.page(int(page_index))

    # 3获取页码列表
    pages = paginator.page_range

    # 4.1获取总页数
    num_pages = paginator.num_pages
    current_num = int(page_index)

    if num_pages <= 10:
        # 总页数小于等于5
        pages = range(1, num_pages + 1)
    elif current_num <= 5:
        # 当前页为前5页
        pages = range(1, 11)
    elif num_pages - current_num <= 4:
        # 當前頁爲後5頁
        pages = range(num_pages - 10, num_pages + 1)
    else:
        # 既不是前5页，也不是后5页
        pages = range(current_num - 5, current_num + 5)


    return  render(request,'sqyc_bi/base_in_company_day.html',
                   {'order_list':company_list,
                    'pages':pages,
                    'city_id':city_id ,
                    'company_name':company_name,
                    't_d':t_d } )



def Other_test(request):
    return  HttpResponse("本功能待开发!")











