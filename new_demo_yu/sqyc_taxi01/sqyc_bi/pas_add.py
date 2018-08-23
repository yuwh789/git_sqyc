import pandas as pd
#from sqyc_bi.data_tools import *
#测试开启
from data_tools import *
# import  data_tools_local  
from sqlalchemy import create_engine
import numpy as np
import time
import datetime
from math import *
from threading import Thread



def yester_pas_add(psy, tdate):
    sql1 = "SELECT city_id,booking_user_id, rider_user_phone, status, channel FROM mysql.order_info t1 WHERE city_id = 44  \
    AND create_date >= '{}' AND create_date < '{}'::date + INTERVAL '1 DAY' AND NOT EXISTS ( SELECT 1 FROM mysql.order_info t2 \
    WHERE city_id = 44 AND create_date < '{}' AND t1.booking_user_id = t2.booking_user_id )GROUP BY 1,2,3,4,5".format(tdate,tdate,tdate)
    df1 = psy.data_r(sql1)
    df1['t_date'] = tdate
    psy.data_s( df1, 't_yester_pas_add')
    
    
    
def run_pas_add():
    date_list = Date_list()
    date_yester = date_list.timedlta(1).strftime("%Y-%m-%d")
    date_yester = '2018-08-20'
    psy = Psyco_handle()
    yester_pas_add(psy, date_yester)
    
    
if __name__ == "__main__":    
    print('start...')
    run_pas_add()
    print('end...')
