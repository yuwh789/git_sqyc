import pandas as pd
from sqyc_bi.data_tools import *
#from data_tools import *
from sqlalchemy import create_engine
import numpy as np
import time
import datetime
from math import *
from sqyc_bi.r3_rck import *


# def Test_files():
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
def deal_div(x,y):
    if y[0] == 0:
        return None
    else:
        return round( x[0]/y[0]-1, 4)

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


    
def  Order_driver_num(t_cityId,t_date):
    psy = Psyco_handle()
    
    # jd 
    sql_jd_ylx =  "SELECT * from drjd_ylx_num('%s', '%s')" %( t_cityId,  t_date)
    sql_jd_nlx =  "SELECT * from drjd_nlx_num('%s', '%s')" %( t_cityId,  t_date)
    df_sql_jd_ylx = psy.data_r(sql_jd_ylx)
    df_sql_jd_nlx = psy.data_r(sql_jd_nlx)
    
    # jd1
    mer_jd = pd.merge(df_sql_jd_ylx, df_sql_jd_nlx, how = 'outer', on=['recmd_status'] )  
    mer_jd.rename(columns = {'num_x':'有', 'num_y':'无'}, inplace = True )
    mer_jd_t =  mer_jd.set_index(['recmd_status']).T.astype(int) 
    mer_jd_t['order_status'] = '接单'
    
    #  wd
    sql_wd_ylx =  "SELECT * from drwd_ylx_num('%s', '%s')" %( t_cityId,  t_date)
    sql_wd_nlx =  "SELECT * from drwd_nlx_num('%s', '%s')" %( t_cityId,  t_date)
    df_sql_wd_ylx = psy.data_r(sql_wd_ylx)
    df_sql_wd_nlx = psy.data_r(sql_wd_nlx)
    
    #  wd1
    mer_wd = pd.merge(df_sql_wd_ylx, df_sql_wd_nlx, how = 'outer', on=['recmd_status'] )  
    mer_wd.rename(columns = {'num_x':'有', 'num_y':'无'}, inplace = True )
    mer_wd_t =  mer_wd.set_index(['recmd_status']).T.astype(int)
    mer_wd_t['order_status'] = '完单'
    
    
    # mer 
    ret_jd_wd = pd.concat([mer_jd_t, mer_wd_t])
    ret_jd_wd['create_date'] = t_date
    ret_jd_wd['update_date'] =  datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
    
    
    # per
    ret_jd_wd.fillna(0, inplace=True)
    ret_jd_wd['total'] = ret_jd_wd['eight_ten_num'] + ret_jd_wd['five_seven_num']+ret_jd_wd['four_num']+ret_jd_wd['gt_eleven_num']+ret_jd_wd['one_num']+ret_jd_wd['three_num']+ret_jd_wd['two_num']

    ret_jd_wd['pro_one']= round(ret_jd_wd['one_num'] /ret_jd_wd['total'], 4) 
    ret_jd_wd['pro_two']= round(ret_jd_wd['two_num'] /ret_jd_wd['total'], 4) 
    ret_jd_wd['pro_three']= round(ret_jd_wd['three_num'] /ret_jd_wd['total'], 4) 
    ret_jd_wd['pro_four']= round(ret_jd_wd['four_num'] /ret_jd_wd['total'], 4) 

    ret_jd_wd['pro_five_seven']= round(ret_jd_wd['five_seven_num'] /ret_jd_wd['total'], 4) 
    ret_jd_wd['pro_eight_ten']= round(ret_jd_wd['eight_ten_num'] /ret_jd_wd['total'], 4) 
    ret_jd_wd['pro_gt_eleven']= round(ret_jd_wd['gt_eleven_num'] /ret_jd_wd['total'], 4) 
    
    # finish
    ret_jd_wd['recmd_status'] = ret_jd_wd.index 
    
    psy.data_s(ret_jd_wd, "t_driver_order_num")
    
    
def Driver_jd_hb_tb(t_d1):
    psy = Psyco_handle()
    # 处理环比
    t_d2 = Date_list().timedlta(2)  
    
    sql1 = "SELECT * from t_driver_order_num where create_date = '{}' and order_status= '接单' and recmd_status = '有' ".format(t_d1) # 处理日
    sql2 = "SELECT * from t_driver_order_num where create_date = '{}' and order_status= '接单' and recmd_status = '有' ".format(t_d2) # 处理日前一天

    sql3 = "SELECT * from t_driver_order_num where create_date = '{}' and order_status= '接单' and recmd_status = '无' ".format(t_d1) # 处理日
    sql4 = "SELECT * from t_driver_order_num where create_date = '{}' and order_status= '接单' and recmd_status = '无' ".format(t_d2) # 处理日前一天
    
    df1 = psy.data_r(sql1)
    df2 = psy.data_r(sql2)
    # df1 = pd.read_sql(sql1, engine)
    # df2 = pd.read_sql(sql2, engine)

    df3 = psy.data_r(sql3)
    df4 = psy.data_r(sql4) 
    # df3 = pd.read_sql(sql3, engine)
    # df4 = pd.read_sql(sql4, engine)
    
    #print("--- 正在处理接单环比数据， 请稍等...")

    res_b  = pd.DataFrame([ [t_d1,  datetime.datetime.now() ,'接单','有' ] ],columns=['create_date','update_date','order_status','recmd_status' ])   # m2  

    res_b2  = pd.DataFrame([ [t_d1,  datetime.datetime.now() ,'接单','无' ] ],columns=['create_date','update_date','order_status','recmd_status' ])   # m2

    res_b["one_hb"] = round( df1['one_num']/df2['one_num'] - 1, 4 )
    res_b["two_hb"] = round( df1['two_num']/df2['two_num'] - 1, 4 )
    res_b["three_hb"] = round( df1['three_num']/df2['three_num'] - 1, 4 )
    res_b["four_hb"] = round( df1['four_num']/df2['four_num'] - 1, 4 )
    res_b["five_seven_hb"]= round( df1['five_seven_num']/df2['five_seven_num'] - 1, 4 )
    res_b["eight_ten_hb"]= round( df1['eight_ten_num']/df2['eight_ten_num'] - 1, 4 )
    res_b['gt_eleven_hb']= deal_div( df1['gt_eleven_num'],  df2['gt_eleven_num']   )   

    res_b2["one_hb"] = round( df3['one_num']/df4['one_num'] - 1, 4 )
    res_b2["two_hb"] = round( df3['two_num']/df4['two_num'] - 1, 4 )
    res_b2["three_hb"] = round( df3['three_num']/df4['three_num'] - 1, 4 )
    res_b2["four_hb"] = round( df3['four_num']/df4['four_num'] - 1, 4 )
    res_b2["five_seven_hb"]= round( df3['five_seven_num']/df4['five_seven_num'] - 1, 4 )
    res_b2["eight_ten_hb"]= round( df3['eight_ten_num']/df4['eight_ten_num'] - 1, 4 )
    res_b2['gt_eleven_hb']= deal_div( df3['gt_eleven_num'],  df4['gt_eleven_num']   )
    
    #print("--- over! %s日接单环比数据处理成功! ---" %t_d1)




    ###############  处理同比 ######################
    #print("")
    #print("--- 正在处理接单同比数据， 请稍候...")
    t_d2 =  Date_list().timedlta(8)      # 同比时间
 

    sql1 = "SELECT * from t_driver_order_num where create_date = '{}' and order_status= '接单' and recmd_status = '有' ".format(t_d1) # t_d1
    sql2 = "SELECT * from t_driver_order_num where create_date = '{}' and order_status= '接单' and recmd_status = '有' ".format(t_d2) # 同比2

    sql3 = "SELECT * from t_driver_order_num where create_date = '{}' and order_status= '接单' and recmd_status = '无' ".format(t_d1) # t_d1
    sql4 = "SELECT * from t_driver_order_num where create_date = '{}' and order_status= '接单' and recmd_status = '无' ".format(t_d2) # 同比2

    df1 = psy.data_r(sql1)
    df2 = psy.data_r(sql2)
    

    df3 = psy.data_r(sql3)
    df4 = psy.data_r(sql4)
    
 

    if len(df2) ==0 or len(df4)==0:
        df2 = df1
        df4 = df3


    # res_tb  = pd.DataFrame([ [t_d1,  datetime.datetime.now() ,'同比' ] ],columns=['create_date','update_date','per_status'])  #m2  


    res_b["one_tb"] = round( df1['one_num']/df2['one_num'] - 1, 4 )
    res_b["two_tb"] = round( df1['two_num']/df2['two_num'] - 1, 4 )
    res_b["three_tb"] = round( df1['three_num']/df2['three_num'] - 1, 4 )
    res_b["four_tb"] = round( df1['four_num']/df2['four_num'] - 1, 4 )
    res_b["five_seven_tb"]= round( df1['five_seven_num']/df2['five_seven_num'] - 1, 4 )
    res_b["eight_ten_tb"]= round( df1['eight_ten_num']/df2['eight_ten_num'] - 1, 4 )
    res_b['gt_eleven_tb']= deal_div( df1['gt_eleven_num'],  df2['gt_eleven_num']   )   
    #res_b


    res_b2["one_tb"] = round( df3['one_num']/df4['one_num'] - 1, 4 )
    res_b2["two_tb"] = round( df3['two_num']/df4['two_num'] - 1, 4 )
    res_b2["three_tb"] = round( df3['three_num']/df4['three_num'] - 1, 4 )
    res_b2["four_tb"] = round( df3['four_num']/df4['four_num'] - 1, 4 )
    res_b2["five_seven_tb"]= round( df3['five_seven_num']/df4['five_seven_num'] - 1, 4 )
    res_b2["eight_ten_tb"]= round( df3['eight_ten_num']/df4['eight_ten_num'] - 1, 4 )
    res_b2['gt_eleven_tb']= deal_div( df3['gt_eleven_num'],  df4['gt_eleven_num']   )


    #print("--- over! %s日接单同比数据处理成功! ---" %t_d1)

    psy.data_s(res_b, 't_driver_num_hb_tb')   # 调用入库方法  占比
    
    psy.data_s(res_b2, 't_driver_num_hb_tb')   # 调用入库方法  环比
    

    #print("********** over! %s日接单数据已成功入库  **********" %t_d1)
    
    #print("")
   


def Driver_wd_hb_tb(t_d1):
    psy = Psyco_handle()
    t_d2 =   Date_list().timedlta(2)  
 
    sql1 = "SELECT * from t_driver_order_num where create_date = '{}' and order_status= '完单' and recmd_status = '有' ".format(t_d1) # 处理日
    sql2 = "SELECT * from t_driver_order_num where create_date = '{}' and order_status= '完单' and recmd_status = '有' ".format(t_d2) # 处理日前一天

    sql3 = "SELECT * from t_driver_order_num where create_date = '{}' and order_status= '完单' and recmd_status = '无' ".format(t_d1) # 处理日
    sql4 = "SELECT * from t_driver_order_num where create_date = '{}' and order_status= '完单' and recmd_status = '无' ".format(t_d2) # 处理日前一天

    df1 = psy.data_r(sql1)
    df2 = psy.data_r(sql2)
    
 
    df3 = psy.data_r(sql3)
    df4 = psy.data_r(sql4)
    
 
    res_b  = pd.DataFrame([ [t_d1,  datetime.datetime.now() ,'完单','有' ] ],columns=['create_date','update_date','order_status','recmd_status' ])   # m2  

    res_b2  = pd.DataFrame([ [t_d1, datetime.datetime.now() ,'完单','无' ] ],columns=['create_date','update_date','order_status','recmd_status' ])   # m2

    # 接单有拉新环比
    res_b["one_hb"] = round( df1['one_num']/df2['one_num'] - 1, 4 )
    res_b["two_hb"] = round( df1['two_num']/df2['two_num'] - 1, 4 )
    res_b["three_hb"] = round( df1['three_num']/df2['three_num'] - 1, 4 )
    res_b["four_hb"] = round( df1['four_num']/df2['four_num'] - 1, 4 )
    res_b["five_seven_hb"]= round( df1['five_seven_num']/df2['five_seven_num'] - 1, 4 )
    res_b["eight_ten_hb"]= round( df1['eight_ten_num']/df2['eight_ten_num'] - 1, 4 )
    res_b['gt_eleven_hb']= deal_div( df1['gt_eleven_num'],  df2['gt_eleven_num']   )  
 

    # 接单无拉新环比
    res_b2["one_hb"] = round( df3['one_num']/df4['one_num'] - 1, 4 )
    res_b2["two_hb"] = round( df3['two_num']/df4['two_num'] - 1, 4 )
    res_b2["three_hb"] = round( df3['three_num']/df4['three_num'] - 1, 4 )
    res_b2["four_hb"] = round( df3['four_num']/df4['four_num'] - 1, 4 )
    res_b2["five_seven_hb"]= round( df3['five_seven_num']/df4['five_seven_num'] - 1, 4 )
    res_b2["eight_ten_hb"]= round( df3['eight_ten_num']/df4['eight_ten_num'] - 1, 4 )
    res_b2['gt_eleven_hb']= deal_div( df3['gt_eleven_num'],  df4['gt_eleven_num']   )

    
    #res_hb.to_sql("t_driver_num_hb_tb", engine, index=False , if_exists='append')
    #print("--- over! %s日完单环比数据处理成功! ---" %t_d1)




    ###############  处理同比 ######################
    #print("")
    #print("--- 正在处理完单同比数据， 请稍候...")
    t_d2 = Date_list().timedlta(8)  # 同比时间
 

    sql1 = "SELECT * from t_driver_order_num where create_date = '{}' and order_status= '完单' and recmd_status = '有' ".format(t_d1) # t_d1
    sql2 = "SELECT * from t_driver_order_num where create_date = '{}' and order_status= '完单' and recmd_status = '有' ".format(t_d2) # 同比2

    sql3 = "SELECT * from t_driver_order_num where create_date = '{}' and order_status= '完单' and recmd_status = '无' ".format(t_d1) # t_d1
    sql4 = "SELECT * from t_driver_order_num where create_date = '{}' and order_status= '完单' and recmd_status = '无' ".format(t_d2) # 同比2


    df1 = psy.data_r(sql1)
    df2 = psy.data_r(sql2)
 
    df3 = psy.data_r(sql3)
    df4 = psy.data_r(sql4)
    
 

    if len(df2) ==0 or len(df4)==0:
        df2 = df1
        df4 = df3

 

    res_b["one_tb"] = round( df1['one_num']/df2['one_num'] - 1, 4 )
    res_b["two_tb"] = round( df1['two_num']/df2['two_num'] - 1, 4 )
    res_b["three_tb"] = round( df1['three_num']/df2['three_num'] - 1, 4 )
    res_b["four_tb"] = round( df1['four_num']/df2['four_num'] - 1, 4 )
    res_b["five_seven_tb"]= round( df1['five_seven_num']/df2['five_seven_num'] - 1, 4 )
    res_b["eight_ten_tb"]= round( df1['eight_ten_num']/df2['eight_ten_num'] - 1, 4 )
    res_b['gt_eleven_tb']= deal_div( df1['gt_eleven_num'],  df2['gt_eleven_num']   ) 
    #res_b

    # 无拉新环比
    res_b2["one_tb"] = round( df3['one_num']/df4['one_num'] - 1, 4 )
    res_b2["two_tb"] = round( df3['two_num']/df4['two_num'] - 1, 4 )
    res_b2["three_tb"] = round( df3['three_num']/df4['three_num'] - 1, 4 )
    res_b2["four_tb"] = round( df3['four_num']/df4['four_num'] - 1, 4 )
    res_b2["five_seven_tb"]= round( df3['five_seven_num']/df4['five_seven_num'] - 1, 4 )
    res_b2["eight_ten_tb"]= round( df3['eight_ten_num']/df4['eight_ten_num'] - 1, 4 )
    res_b2['gt_eleven_tb']= deal_div( df3['gt_eleven_num'],  df4['gt_eleven_num']   )


       
    psy.data_s(res_b, 't_driver_num_hb_tb')   # 调用入库方法  环比
    psy.data_s(res_b2, 't_driver_num_hb_tb')   # 调用入库方法  环比
    # res_b.to_sql("t_driver_num_hb_tb", engine, index=False , if_exists='append')

    # res_b2.to_sql("t_driver_num_hb_tb", engine, index=False , if_exists='append')
    
    #print("********** over! %s日完单数据已处理  **********" %t_d1)

   
    
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
    time.sleep(2)
    company_list = ["交运"]
    for company in company_list:
        Test_cany_day(t_date, 113, company)



def Run_driver_num():
    t_date = Date_list().timedlta(1)
    Order_driver_num('44', t_date)


def Run_hb_tb():
    t_d = Date_list().timedlta(1)
    Driver_jd_hb_tb(t_d)
    Driver_wd_hb_tb(t_d)
    
def Run_risk():
    take_driver_num = 0.2  # 订单异常之 接驾异常参数  
    service_num = 0.2  # 订单异常之 服务常参数  
    order_interval_num = 0.2  # 订单异常之 两单间隔参数
    driver_exception_value = 0.35   # 司机异常系数
    args_value = 0.5    # 订单异常数值一级
    passenger_value = 0.15 


    Run_risk_info()



if __name__ == "__main__":
    Run_driver_num()
    Run_hb_tb()

