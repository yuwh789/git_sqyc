import pandas as pd
from math import *
import numpy as np
import pymysql
import time
import  re
import datetime
# import matplotlib.pyplot as plt
from sqlalchemy import create_engine

import smtplib  ,time # 邮件使用库
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.header import Header  # 给对象进行编码
from email.mime.application import MIMEApplication # MIME程序类型,适用多种类型:如文本,图片,xlsx, MP3音频等
from django.conf import settings


class Psyco_handle(object):
    def __init__(self):
        self.database_name = "taxidb"
        self.connect_ip = "localhost"
        self.connect_port = 5432
        self.user_name = "taxiuser"
        self.pwd = "taxiuser"
        pass

    def data_s(self, dtFme, t_table):
        try:

            in_engine = "postgresql://%s:%s@%s:%s/%s" % (
            self.user_name, self.pwd, self.connect_ip, self.connect_port, self.database_name)

            self.engine = create_engine(in_engine)

            dtFme.to_sql(t_table, self.engine, index=False, if_exists="append")

            print("%s---Files save by Postgre !" % (time.strftime("%Y-%m-%d %H:%M", time.localtime())))

        except Exception as e:

            print("连接数据库发现异常", e)

            return "Postgre has gone away --- %s " % (time.strftime("%Y-%m-%d %H:%M", time.localtime()))

        return self.engine

    def data_r(self, insql):

        try:
            in_engine = "postgresql://%s:%s@%s:%s/%s" % (
            self.user_name, self.pwd, self.connect_ip, self.connect_port, self.database_name)
            self.engine = create_engine(in_engine)
            self.df = pd.read_sql(insql, self.engine)
        except Exception as e:
            print("连接数据库异常", e)
            return e
        return self.df


class Date_list(object):

    def date_list(self):
        print("当前时间为: ", time.strftime("%Y-%m-%d %H:%M"))
        # 日期范围列表
        t_d1 = input("请输入开始日期(默认昨日):")
        a_day = datetime.timedelta(days=1)  # time
        if t_d1 == "":
            t_d1 = datetime.datetime.now() - a_day

        else:
            date_list = [t_d1]
            t_d1 = datetime.datetime.strptime(t_d1, "%Y-%m-%d")  #

        t_d2 = input("请输入结束日期(默认前者):")
        if t_d2 == "":
            t_d2 = t_d1
        else:
            t_d2 = datetime.datetime.strptime(t_d2, "%Y-%m-%d")
        date_list = [datetime.datetime.strftime(t_d1, "%Y-%m-%d")]

        while t_d1 != t_d2:
            t_d1 = t_d1 + a_day
            date_list.append(datetime.datetime.strftime(t_d1, "%Y-%m-%d"))
        print('加载时间范围为:', date_list)
        # print("")
        return date_list

    def timedlta(self,inday):
        return datetime.datetime.now() - datetime.timedelta(days=int(inday))






# 经度1，纬度1，经度2，纬度2 （十进制度数） lon1, lat1, lon2, lat2
def Distance(df):
        # 将十进制度数转化为弧度
        # math.degrees(x):为弧度转换为角度
        # math.radians(x):为角度转换为弧度
        if df['fact_end_point'] is not None and df['fact_start_point'] is not None:
            lat1 = float( df['fact_start_point'].split(',')[1] ) # A维度
            lon1 = float( df['fact_start_point'].split(',')[0] ) # A经度
            lat2 =  float( df['fact_end_point'].split(',')[1] )  # B维度
            lon2 =  float( df['fact_end_point'].split(',')[0] )  # B经度
            lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])
            # haversine公式
            dlon = lon2 - lon1
            dlat = lat2 - lat1
            a = sin( dlat /2 ) **2 + cos(lat1) * cos(lat2) * sin( dlon /2 ) **2
            c = 2 * asin( sqrt(a) )
            r = 6371 # 地球平均半径，单位为公里
            return c * r*1000
        else :
            return None

# 经纬度处理002
def Distance2(df):
    if df['driver_coordinate'] is not None and df['fact_start_point'] is not None :
        lat1 = float( df['fact_start_point'].split(',')[1] ) # A维度
        lon1 = float( df['fact_start_point'].split(',')[0] ) # A经度
        lat2 =  float( df['driver_coordinate'].split(',')[1] )  # B维度
        lon2 =  float( df['driver_coordinate'].split(',')[0] )  # B经度
        lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])
        # haversine公式
        dlon = lon2 - lon1
        dlat = lat2 - lat1
        a = sin( dlat /2 ) **2 + cos(lat1) * cos(lat2) * sin( dlon /2 ) **2
        c = 2 * asin( sqrt(a) )
        r = 6371 # 地球平均半径，单位为公里
        return c * r*1000
    else :
        return None



# 接驾异常
def exc_j(df,x):
        if df['接驾秒']<120 or df['接驾里程']<100:
            return 1*x
        else:
            return 0

# 服务异常
def exc_fw(df,x):
        if df['行驶分钟']<2 or df['服务里程']<1000:
            return 1*x
        else:
            return 0



# 两单间隔异常
def exc_ldjg(df,x):
    if df['间隔里程'] != '' and  df['间隔里程'] !='/' :
        if df['间隔分钟'] <2 or df['间隔里程'] < 100:
            return 1*x
        else:
            return 0
    else:
        return 0


# 风控多次握手
def exc_dcws(df ): # 多次握手异常
    if df['max_num'] >=7:
        return 1
    elif df['max_num'] >= 6:
        return 0.7
    elif df['max_num'] >=5:
        return 0.6
    elif df['max_num'] >=4:
        return 0.5
    elif df['max_num'] >=3:
        return 0.4
    elif df['max_num'] >=2:
        return 0.1
    else:
        return 0



#风控中位数评分
def  func_money(df):
    if df['线上总额'] >= df['线上总额中位数'] *10:
        return 0.2
    elif  df['线上总额'] >= df['线上总额中位数'] *2:
        return -0.4
    elif df['线上总额'] >= df['线上总额中位数'] :
        return -0.2
    elif df['线上总额'] < df['线上总额中位数'] :
        return 0



# 根据拉新指标，调整评分, 多次握手异常为0
def ret_newScore(df):
    if (( df['status']==3.0) | ( df['status']==4.0 )) and df['多次握手异常']==0 :
        return  max( (df['风险评分'] - 0.5), 0)
    else:
        return df['风险评分']


def add_file(att_path):
    #  将对象仅限编码
    from email.header import Header  # 给对象进行编码
    from email.mime.application import MIMEApplication  #
    with open(att_path,'rb') as f:
        msg_application= MIMEApplication(f.read())
    files_name = Header(att_path.split('/')[-1], 'utf-8').encode()  # no header alreadly ok?
    msg_application.add_header('Content-Disposition', 'attachment', filename= files_name)
    return  msg_application
    pass


def mail_mimemuprt( t_d_text, att_path,to_address_list ):
    from django.conf import settings
    from django.core.mail import EmailMultiAlternatives
    from django.core import  mail

    from_email = settings.EMAIL_HOST_USER
    # subject 主题 content 内容 to_addr 是一个列表，发送给哪些人
    content = '致好：\n   附件为：%s ， 请查收， 谢谢！' %(t_d_text)

    # 发送信息，  发送参数
    msg = mail.EmailMessage(t_d_text, content, from_email, to_address_list )
    #msg.content_subtype = "html"
    #msg.encoding = 'utf-8'

    # 添加附件（可选）
    att_path = add_file(att_path)
    msg.attach( att_path )  # att_path为：txt附件

    # 发送
    msg.send()
    print('ok~')


