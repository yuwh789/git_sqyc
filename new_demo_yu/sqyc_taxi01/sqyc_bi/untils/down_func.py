from django.http import  HttpResponse
import  csv
from sqyc_bi.data_tools import  *

# 方法共分为三种--1针对ORM框架 --
# 2 直接访问connection方法(手动传入字典方式字段名--较为单一 但是方便权限限制)
# 3 直接访问方法(传入系统查询所有字段名--函数自动解析-- 方便但放开了所有字段)
# response['Content-Type'] = 'application/vnd.ms-excel'
def Down_files(request, order_list, **kwargs ):
    # Create the HttpResponse object with the appropriate CSV header.
    response = HttpResponse(content_type='APPLICATION/OCTET-STREAM')
    response['Content-Disposition'] = 'attachment; filename="download_files.csv"'

    writer = csv.writer(response)
    # 取出城市代码,写入csv文件
    the_name = request.session['user_name'].split("_")[-1]
    writer.writerow([the_name])

    title_list = []  #保存字典的key
    value_list=[]  # 保存字典的value
    for k,v in kwargs.items():
        title_list.append(v)  # 保存字典的v
        value_list.append(k)  # 保存字典的k
    writer.writerow( title_list )

    for i in order_list:
        # writer.writerow([i.create_date, i.recmd_status, i.order_status ])  # 这里的i.create属性
        writer.writerow(  [ getattr(i,j) for j in value_list ]   )
    return response


def Down_files_dic(request, order_list, **kwargs ):
    # Create the HttpResponse object with the appropriate CSV header.
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="download_files.csv"'

    writer = csv.writer(response)
    # 取出城市代码, 写入csv文件。
    the_name = request.session['user_name'].split("_")[-1]
    writer.writerow([the_name])

    title_list = []  #保存字典的key
    value_list=[]  # 保存字典的value
    for k,v in kwargs.items():
        title_list.append(v)  # 保存字典的v
        value_list.append(k)  # 保存字典的k
    writer.writerow( title_list )

    for i in order_list:
        # writer.writerow([ i['dr_name'], i['dr_id'], i['order_cnt'] ])  # i ~ tuple
        writer.writerow(  [ i[j] for j in value_list ]   )

    return response


def Down_files_dic2(request, order_list, colname ):
    #  改写， 直接由列表名自行解析判断
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="downloads.csv"'

    writer = csv.writer(response)
    the_user_name = request.session['user_name'].split("_")[-1]  # 取出城市代码, 写入csv文件。

    writer.writerow([the_user_name])
    writer.writerow( colname )

    for i in order_list:
        writer.writerow(  [ i[j] for j in colname ] )

    return response


def mail_mimemuprt_n(sql, par_name,to_add):
    psy = Psyco_handle()
    df1 = psy.data_r(sql)
    t_d = datetime.datetime.now().strftime("%m-%d %H:%M:%S")
    path = r'/home/dev/virtualenv_files/t_demo1/数据_{}_{}.xlsx'.format(par_name,t_d)
    df1.to_excel(path)

    to_add_list = ['yuweihong@01zhuanche.com', ]
    for i in to_add.split(','):
        to_add_list.append(i)
    mail_mimemuprt('需求数据整理', path, to_add_list)