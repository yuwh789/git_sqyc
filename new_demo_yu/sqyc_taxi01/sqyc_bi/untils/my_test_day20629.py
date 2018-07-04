import pandas as pd
#from sqyc_bi.untils.data_tools import *
from sqyc_bi.data_tools import *
from sqlalchemy import create_engine
import numpy as np
import time
import datetime
from math import *


# def Test_files():
#     print(order_info_data.head())
#     print(order_info_data.dtypes)
#
#     # 对每一位用户的订单进行排序
#     order_info_data_ordered = order_info_data.sort_values(by=['user_id', 'order_id'], ascending=True)
#     print(order_info_data_ordered.head(10))
#
#     # 新增辅助列计算当前订单是用户的第几单
#     order_info_data_ordered['order_time'] = 1
#     order_info_data_ordered['order_times'] = order_info_data_ordered.groupby('user_id').agg({'order_time': 'cumsum'})[
#         'order_time']
#
#     # 将原始表复制一遍并将第几比订单做一下处理
#     order_info_data_ordered_2 = order_info_data_ordered.loc[:, ['user_id', 'end_time', 'order_times']]
#     order_info_data_ordered_2['order_times'] = order_info_data_ordered_2['order_times'] + 1
#     print(order_info_data_ordered_2.head(10))
#     order_info_data_ordered_2.rename(columns={'end_time': 'last_end_time'}, inplace=True)
#
#     # 将两个数据表合并
#     merge_data = order_info_data_ordered.merge(right=order_info_data_ordered_2,
#                                                how='left', on=['user_id', 'order_times']).loc[:,
#                  ['user_id', 'order_id', 'start_time', 'end_time', 'last_end_time']]
#
#     merge_data['last_end_time'] = merge_data['last_end_time'].fillna('第一单')
#     print(merge_data)


def Test_cany_day(t_date, t_cityId, t_canyName):
    psy = Psyco_handle()
    sql = "SELECT t1.*, t2.rard_punish_money  from fuc_company_day('%s', '%s', '%s')  t1 \
    LEFT JOIN  fuc_driver_reward('%s','%s','%s') t2 on t1.司机编码::varchar = t2.driv_id::varchar" %(t_date,t_cityId,t_canyName,t_date,t_cityId,t_canyName)
    df_company_day = psy.data_r(sql)
    df_company_day.fillna("0", inplace=True)
    df_company_day.rename(
        columns={"城市编码": "city_id", "城市": "city", "司机编码": "driver_id", "司机姓名": "driver_name", "司机电话": "driver_phone",
                 "分公司编码": "taxi_company_id", "分公司名称": "taxi_company_name", "车牌号": "plate_number", "证件号": "id_number",
                 "sum_online": "total_online_minute", "rard_punish_money": "reward_punish_money"}, inplace=True)
    df_company_day["t_date"] = t_date
    df_company_day["update_date"] = time.strftime("%Y-%m-%d %H:%M", time.localtime())
    df_company_day["id"] = 1
    psy.data_s(df_company_day, "t_company_day_data")




def run_company_day():
    # Test_cany_day("2018-06-10",94,"大众")
    date_list = Date_list()
    # time  handle
    t_date = date_list.timedlta(1)


    # === 哈尔滨数据
    company_list = ["大众", "天鹅", "现代", "飞达"]  # 四家公司   8:30
    for company in company_list:
        Test_cany_day(t_date, 94, company)


    #  === 温州数据
    time.sleep(3)
    company_list = ["交运"]
    for company in company_list:
        Test_cany_day(t_date, 113, company)



if __name__ == "__main__":
    # Test_cany_day("2018-06-10",94,"大众")
    date_list = Date_list()
    # time  handle
    t_date = date_list.timedlta(1)


    # === 哈尔滨数据
    company_list = ["大众", "天鹅", "现代", "飞达"]  # 四家公司   8:30
    for company in company_list:
        Test_cany_day(t_date, 94, company)


    #  === 温州数据
    time.sleep(3)
    company_list = ["交运"]
    for company in company_list:
        Test_cany_day(t_date, 113, company)
