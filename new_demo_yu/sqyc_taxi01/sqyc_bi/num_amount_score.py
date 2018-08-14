import pandas as pd
from sqyc_bi.data_tools import *
#from data_tools import *  # 测试开启
# import  data_tools_local
from sqlalchemy import create_engine
import numpy as np
import time
import datetime
from math import *


def Respon_cancel_num(psy, t_date, t_cityId):
    sql = "SELECT city_id, driver_id, sum(case when t1.driver_id is not null then 1 else 0 end) res_cnt, \
    sum(case when reason_type=2  and status=60  and driver_id is not null  then 1 else 0 end )  dr_cancel_num, \
    sum(case when reason_type=1 and status=60  and driver_id is not null  then 1 else 0 end )  pass_cancel_num  from order_info t1 \
    where (t1.create_date >= '{}'::date and t1.create_date < '{}'::date + interval '1 day') and city_id = {}  \
    and driver_id is not null GROUP BY 1,2".format(t_date, t_date, t_cityId)
    res_can_num = psy.data_r(sql)
    return res_can_num


def online_num_amount(psy, t_date, t_cityId):
    sql = "SELECT driver_id, sum( case when  t1.pay_method in (1, 4, 5, 6, 7) then 1 else 0 end  ) ol_num ,  \
    sum( case when ( t1.pay_type is not null or (t1.pay_method in (1, 4, 5, 6, 7) and t1.fact_pay_amount = 0  ) ) \
    then t1.dis_count_amount+ t1.fact_pay_amount  else 0 end  ) ol_amount, count(*) com_cnt_order  from order_info t1  \
    where t1.service_end_date >= '{}'::date and t1.service_end_date< '{}'::date + interval '1 day'  \
    and t1.city_id ={}  and t1.status = 50  GROUP BY 1".format(t_date, t_date, t_cityId)
    onl_num_amo = psy.data_r(sql)
    return onl_num_amo


def Appra_score(psy, t_date):
    sql = "SELECT driver_id,count(*) ara_total_num,  sum( case when appraisal_score = 5 then 1 else 0 end ) high_num, \
    sum(case when appraisal_score in (1,2) then 1 else 0 end ) low_num \
    from order_appraisal  where create_date >= '{}' and create_date< '{}'::date + interval '1 day' GROUP BY 1 ".format(
        t_date, t_date)
    apr_sco = psy.data_r(sql)
    return apr_sco


def Run_num_amount_score(t_cityId, t_canyName):
    # t_cityId = 44
    # t_canyName = '银建|金建'

    psy = Psyco_handle()
    date_list = Date_list().date_list()
    for t_date in date_list:
        df_resCaNu = Respon_cancel_num(psy, t_date, t_cityId)
        df_onlNuAm = online_num_amount(psy, t_date, t_cityId)
        apr_sco = Appra_score(psy, t_date)

        mer_res_onl = pd.merge(df_resCaNu, df_onlNuAm, how='left', on=['driver_id'])
        mer_res_onl_apr = pd.merge(mer_res_onl, apr_sco, how='left', on=['driver_id'])
        mer_res_onl_apr.fillna(0, inplace=True)
        mer_res_onl_apr['t_d'] = t_date
        psy.data_s(mer_res_onl_apr, 't_num_amount_score')


if __name__ == '__main__':
    Run_num_amount_score(44, '银建|金建')