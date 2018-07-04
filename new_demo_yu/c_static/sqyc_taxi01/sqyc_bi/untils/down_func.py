from django.http import  HttpResponse
import  csv


def Down_files(request, order_list, **kwargs ):
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
        # writer.writerow([i.create_date, i.recmd_status, i.order_status ])  # 这里的i才具有create那些属性
        writer.writerow(  [ getattr(i,j) for j in value_list ]   )

    return response

class down_demo():
    def __init__(self,request,order_list):
        self.response = HttpResponse(content_type='text/csv')
        self.response['Content-Disposition'] = 'attachment; filename="download_files.csv"'
        self.order_list = order_list
        self.writer = csv.writer(self.response)

    def title_data(self, str1, str2):
        key_list = []  # 保存字典的key
        value_list = []  # 保存字典的value

        self.str1 = str1.split(",")
        self.writer.writerow(self.str1)


        self.writer.writerow(key_list)
