import  pandas as pd
from math import *
import numpy as np
import pymysql
import time
import datetime
#import matplotlib.pyplot as plt
from sqlalchemy import create_engine






class Psyco_handle(object):
    def __init__(self):
        self.database_name = "taxidb"
        self.connect_ip = "localhost"
        self.connect_port = 5432
        self.user_name = "taxiuser"
        self.pwd="taxiuser"
        pass
    
    def  data_s(self,dtFme,t_table):
        try:
            
            in_engine = "postgresql://%s:%s@%s:%s/%s" %(self.user_name, self.pwd, self.connect_ip,self.connect_port, self.database_name)
            
            self.engine = create_engine(in_engine)
            
            dtFme.to_sql(t_table,self.engine, index=False, if_exists="append")
            
            print("%s---Files save by Postgre !" %( time.strftime( "%Y-%m-%d %H:%M", time.localtime() )  ))
            
        except Exception as e:
            
            print("连接数据库发现异常", e)
            
            return "Postgre has gone away --- %s "  %( time.strftime( "%Y-%m-%d %H:%M", time.localtime() )  )
        
        return self.engine   
    
    def data_r(self,insql):
        
        try:
            in_engine = "postgresql://%s:%s@%s:%s/%s" %(self.user_name, self.pwd, self.connect_ip,self.connect_port, self.database_name)
            self.engine = create_engine(in_engine)
            self.df = pd.read_sql(insql,self.engine )
        except Exception as e:
            print("连接数据库异常",e)
            
        return  self.df






class Date_list(object):

    def date_list():
        print("当前时间为: ", time.strftime("%Y-%m-%d %H:%M") )
        # 日期范围列表
        t_d1 = input("请输入开始日期(默认昨日):")  
        a_day = datetime.timedelta(days=1)  # time
        if t_d1 =="":   
            t_d1 = datetime.datetime.now()  -  a_day  

        else :
            date_list=[t_d1 ]
            t_d1 = datetime.datetime.strptime(t_d1,"%Y-%m-%d") # 

        
        t_d2 = input("请输入结束日期(默认前者):")  
        if t_d2 =="":
            t_d2= t_d1
        else:
            t_d2= datetime.datetime.strptime(t_d2,"%Y-%m-%d")
        date_list=[datetime.datetime.strftime(t_d1,"%Y-%m-%d") ]   
        
        
        while t_d1 != t_d2:
            t_d1 = t_d1 + a_day
            date_list.append(datetime.datetime.strftime(t_d1,"%Y-%m-%d") )
        print('加载时间范围为:',date_list)
        #print("")
        return date_list

    def timedlta(inday):
        return datetime.datetime.now()  - datetime.datetime.timedelta( days=int(inday) )
