import pandas as pd
from sqyc_bi.data_tools import *
#测试开启
#from data_tools import *
# import  data_tools_local  
from sqlalchemy import create_engine
import numpy as np
import time
import datetime
from math import *
from threading import Thread



def ser_passengeer(psy, t_date1, t_date2, result):
    sql = "SELECT  booking_user_id, rider_user_phone as user_phone, max(service_end_date) max_ser_date  \
    from mysql.order_info  where city_id = 44 and  service_end_date >= '{}' \
    and service_end_date < '{}' and  status = 50  GROUP BY 1,2 ".format(t_date1,t_date2)
    ser_pas = psy.data_r(sql)
    result.append(ser_pas)
    

def yester_new_pas(psy,sdate,result):
    sql = "select booking_user_id, rider_user_phone, max(create_date) max_create from mysql.order_info where city_id=44 \
    group by 1,2 having max(create_date) >='{}' and max(create_date)<'{}'::date + interval '1 day'".format(sdate,sdate)    
    new_pas = psy.data_r(sql)
    result.append(new_pas)
 
    
def run_ser_pas():

    date_list = Date_list()
    date_now = datetime.datetime.now().strftime("%Y-%m-%d")
    date_mid = date_list.timedlta(14).strftime("%Y-%m-%d")
    date_fr = date_list.timedlta(28).strftime("%Y-%m-%d")
    date_yester = date_list.timedlta(1).strftime("%Y-%m-%d")
    psy = Psyco_handle()
    
    result = []
    
    df1 = Thread(target=ser_passengeer, args=(psy, date_mid, date_now, result) )
    df2 = Thread(target=ser_passengeer,args =(psy, date_fr, date_mid, result))
    #df3 = Thread(target=yester_new_pas, args=(psy,date_yester,result))
    df1.start()
    time.sleep(1)
    df2.start()
    time.sleep(3)
    #df3.start()
    df1.join()
    df2.join()
    #df3.join()
    # print( '当前result的长度为:',len(result) )
    
    
    res_mid_now = result[0]
    res_mid_now['update_date']= datetime.datetime.now()
    res_fr_mid = result[1]
    res_fr_mid['update_date']= datetime.datetime.now()

    psy.data_s(res_mid_now, 't_last_ser_pas')
    time.sleep(1)
    psy.data_s(res_fr_mid, 't_last_ser_pas')

    #df3.join()
    #res_yester = result[2]
    #res_yester['update_date'] = datetime.datetime.now()
    #psy.data_s(res_yester, 't_yester_new_pas')
    
if __name__ == "__main__":
    print('start...')
    run_ser_pas()
    print('over...')
    
    
