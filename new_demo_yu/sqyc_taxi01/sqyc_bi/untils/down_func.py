from django.http import  HttpResponse
import  csv


def Down_files(request, order_list, **kwargs ):
    # Create the HttpResponse object with the appropriate CSV header.
    response = HttpResponse(content_type='APPLICATION/OCTET-STREAM')
    response['Content-Disposition'] = 'attachment; filename="download_files.csv"'

    writer = csv.writer(response)
    # 取出城市代码, 写入csv文件。
    the_name = request.session['user_name'].split("_")[-1]
    writer.writerow([the_name])
       # To_do_list

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
       # To_do_list

    title_list = []  #保存字典的key
    value_list=[]  # 保存字典的value

    for k,v in kwargs.items():
        title_list.append(v)  # 保存字典的v
        value_list.append(k)  # 保存字典的k

    writer.writerow( title_list )

    for i in order_list:
        # writer.writerow([i.create_date, i.recmd_status, i.order_status ])  # 这里的i.create属性
        writer.writerow(  [ i[j] for j in value_list ]   )

    return response


def Down_files_dic2(request, order_list, colname ):
    #  改写， 直接由列表名自行解析判断

    response = HttpResponse(content_type='text/csv')

    response['Content-Disposition'] = 'attachment; filename="downloads.csv"'

    writer = csv.writer(response)
    # 取出城市代码, 写入csv文件。
    the_name = request.session['user_name'].split("_")[-1]
    writer.writerow([the_name])
       # todo

    writer.writerow( colname )

    for i in order_list:
        # writer.writerow([i.create_date, i.recmd_status, i.order_status ])  # 这里的i.create属性
        writer.writerow(  [ i[j] for j in colname ] )

    return response
