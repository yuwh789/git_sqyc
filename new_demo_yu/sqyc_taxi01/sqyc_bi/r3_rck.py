import pandas as pd
#测试开启
from sqyc_bi.data_tools import *
from sqlalchemy import create_engine
import numpy as np
import time
import datetime
from math import *




def Risk_record(t_d,psy):
    print('--- 正在处理: 司机记录指标 ---')
    sql_fkDr  = "select remark, city_id,user_id, user_phone, create_time, warn_type  from mysql.risk_refuse_log  \
    where  create_time  >= '{}' and create_time < '{}'::date + INTERVAL '1 day' and warn_type ~ 'SMS|DRIVER_FOZEN' ".format(t_d,t_d)
    df_fkDr = psy.data_r(sql_fkDr)
    return df_fkDr


def Df_drInfo(t_d,psy):
    # 处理司机异常
   
    # 当日司机完单总量
    sql_num_total = " SELECT t1.*  from (SELECT t1.city_id, t1.driver_id,  COUNT(*) 完单总量 from mysql.risk_order t1 where t1.city_id is not \
    null  and t1.pay_card_no is not null  and t1.fact_start_date < '{}'::date + INTERVAL '1 day' \
    GROUP BY 1 ,2   HAVING COUNT(*)>2  ) t1 join  (SELECT DISTINCT driver_id from mysql.risk_order t2 \
    where  fact_start_date >=  '{}' and  fact_start_date < '{}'::date + INTERVAL '1 day' ) t2 on  t2.driver_id = t1.driver_id  ".format(t_d, t_d,t_d)
    
    
    # 当日司机支付账号多次握手订单   create_time
    sql_num_pay = " SELECT a1.city_id, a1.driver_id, SUM(a1.num) 多次握手订单  \
    FROM (SELECT t1.city_id, t1.driver_id, t1.pay_card_no, COUNT(*) num from mysql.risk_order t1 where t1.city_id is not null  and t1.pay_card_no is not null \
    and   t1.fact_start_date   <= '{}'::date + INTERVAL '1 day'	GROUP BY 1 ,2,3 HAVING COUNT(*)>2	) a1 JOIN  \
    ( SELECT distinct  t2.driver_id  from mysql.risk_order  t2  where  fact_start_date >='{}' and  fact_start_date < '{}'::date + INTERVAL '1 day' ) a2  on a1.driver_id = a2.driver_id  GROUP BY 1 ,2".format(t_d,t_d,t_d)
    
    
    print('--- 司机信息指标 ---')
    df_drInfo_total = psy.data_r(sql_num_total)
    
    print("--- 多次握手订单指标 ---")
    df_dfInfo_pay = psy.data_r(sql_num_pay)
    
    
    driver_exception_value = 0.35   # 司机异常系数
    df_drInfo = pd.merge(df_drInfo_total,df_dfInfo_pay, how='left', on=['driver_id','city_id'])
    df_drInfo['司机异常'] = ( df_drInfo['多次握手订单']/df_drInfo['完单总量'])* driver_exception_value
    return df_drInfo


def Df_lx(t_d,psy):
    # 处理司机拉新
    print('---  拉新数据指标 --- ')
    sql_lx= "SELECT  * from car_biz_driver_recommend where expires_date  >= '{}' ".format(t_d)  
    df_lx = psy.data_r(sql_lx)
    return df_lx


def Fk_seven_data(t_d,psy):
    # 处理风控七日数据
    print('--- 风控七天订单数据 ---')
    sql = " select city_id ,order_no,driver_id,fact_start_date as create_date ,remark,booking_user_phone,device_id,pay_card_no  from mysql.risk_order  \
    where fact_start_date > '{}'::date - INTERVAL '7 day'  and  fact_start_date < '{}'::date + INTERVAL '1 day'  and city_id is not null  ".format(t_d,t_d)
    # ps 由于create_time 是风控系统创建时间, 会晚于订单创建, 订单实际出发时间, 故而建议用fact_start_date 更合适.
    df1 = psy.data_r(sql)  # 接单数据

    # 设备握手频次处理
    df1['device_id_f'] = df1['device_id']
    df1['device_id_f'].replace('null', 'np.nan' , inplace=True)
    d_device = df1.groupby(['driver_id', 'device_id_f']).size().reset_index()
    d_device.rename(columns={0:'d_device_num'}, inplace=True )
    res= pd.merge(df1, d_device ,how = 'left', on = [ 'driver_id','device_id_f'] )
    res.drop('device_id_f', axis=1, inplace=True)

    # 手机号握手频次处理
    d_phone = df1.groupby(['driver_id','booking_user_phone']).size().reset_index() 
    d_phone.rename(columns = {0:'d_phone_num'} , inplace=True) # 修改列名
    # d_phone = d_phone.sort_values( by = ['num'] ,ascending=False )  # 结果处理, 为下一步合并使用
    res = pd.merge( res, d_phone, how='left', left_on= ['driver_id','booking_user_phone'] , right_on = ['driver_id','booking_user_phone'] )

    #  支付账号握手频次处理
    d_payCard = df1.groupby(['driver_id','pay_card_no']).size().reset_index()
    d_payCard.rename(columns = {0:'d_payCard_num'}, inplace= True)
    res = pd.merge(res, d_payCard, how='left', left_on = ['driver_id','pay_card_no'], right_on = ['driver_id','pay_card_no' ])

    res['max_num'] = res[['d_device_num','d_payCard_num','d_phone_num']].apply(np.max, axis =1)  # 处理最大频次
    return res



def Passenger_info(t_d,psy):
    # 乘客异常 15% , 乘客完单数和接单司机比例70,if 完单数<=2 则 0 else  比例*50, 去掉0.7
    # create_time  ---> fact_start_date
    print("--- 乘客异常数据 ---")
    sql_ck_num = "SELECT t1.pay_card_no, COUNT(*)  乘客完单数 , COUNT(DISTINCT t1.driver_id)   对接司机数  from  \
    ( SELECT pay_card_no,driver_id,booking_user_id from  mysql.risk_order  where   fact_start_date <  '{}'::date + INTERVAL '1 day' and pay_card_no is not null ) t1  join  \
    (SELECT distinct  booking_user_id  from  mysql.risk_order   where   pay_card_no is not null  and (fact_start_date  >='{}'  and fact_start_date< '{}'::date + INTERVAL '1 day' )  )   t2   \
    on t1.booking_user_id = t2.booking_user_id  GROUP BY 1   HAVING COUNT(*) >2 ".format(t_d,t_d,t_d)
    df_ck_num = psy.data_r(sql_ck_num)

    # 乘客异常
    passenger_value = 0.15   # 乘客异常数值
    df_ck_num['乘客异常'] =( 1-  (df_ck_num['对接司机数']/df_ck_num['乘客完单数'] ) )*passenger_value

    return df_ck_num




def Order_online(t_d,psy,fk_s_d):
    
    sql1 = "SELECT t1.* ,a2.driver_coordinate,a2.grab_order_time,( extract(epoch FROM t1.fact_start_date) - extract(epoch FROM a2.grab_order_time ) )  as 接驾秒 , ( extract(epoch FROM t1.fact_end_date) - extract(epoch FROM t1.fact_start_date) )/60 as 行驶分钟 \
    from (	select  order_id,driver_id,  city_id,service_end_date,driver_name,booking_user_id,rider_user_phone,  \
    fact_pay_amount ,fact_start_point,fact_end_point,dis_count_amount,fact_start_date,fact_end_date  from  mysql.order_info  where  ( service_end_date >= '{}'   \
    and  service_end_date < '{}'::date  + INTERVAL '1 day')) t1  join ( SELECT order_id from mysql.order_settle_detail where pay_status=1 and online_pay_status=1 ) t2   \
    on  t1.order_id = t2.order_id  left join  (  SELECT order_id,  driver_id, driver_coordinate, MIN( grab_order_time ) grab_order_time   from  mysql.order_driver_event  \
    where grab_order_time  >= '{}'  and  grab_order_time < '{}'::date  + INTERVAL '1 day' 	GROUP BY 1,2,3 	) a2  \
    on t1.order_id = a2.order_id and t1.driver_id = a2.driver_id ".format(t_d,t_d, t_d, t_d)

    sql2 ="SELECT * from  diff_time_point('{}') ".format(t_d)

    print('---  接驾数据, 服务数据  --- ') 
    df_onDay = psy.data_r(sql1)
    
    print('---  订单间隔数据  --- ') 
    df_onDay2 = psy.data_r(sql2)

    df_onDay['服务里程'] = df_onDay.apply(Distance,axis =1)
    df_onDay['接驾里程'] = df_onDay.apply( Distance2,axis=1)
    df_onDay2['fact_end_point'] = df_onDay2['上一单服务结束位置']
    df_onDay2['间隔里程'] = df_onDay2.apply(Distance,axis=1)

    take_driver_num = 0.2  # 订单异常之 接驾异常参数  
    service_num = 0.2  # 订单异常之 服务常参数  
    order_interval_num = 0.2  # 订单异常之 两单间隔参数
    args_value = 0.5    # 订单异常数值一级

    #print("")
    print('--- 订单异常: 接驾异常,服务异常, 间隔异常, 金额异常 ---')
    
    res_xs = pd.merge(df_onDay, df_onDay2 , how='left', on =['order_id'])  # 整合主表
    ret_xs = res_xs[['order_id','city_id','service_end_date','driver_id','driver_name','booking_user_id','rider_user_phone','fact_pay_amount',
                    'dis_count_amount','接驾秒','接驾里程','行驶分钟','服务里程','间隔分钟','间隔里程']]
    
    ret_xs = pd.merge(ret_xs,fk_s_d[['order_no','max_num','pay_card_no']] , 
                      how = 'left',left_on=['order_id'],right_on=['order_no'] ) # 握手频次
    ret_xs = ret_xs.drop('order_no',axis=1)

    # 总额--总额中位数--金额异常
    ret_xs['线上总额'] = ret_xs['fact_pay_amount'] + ret_xs['dis_count_amount']
    df_onDay_med = ret_xs.groupby('city_id',as_index=False).agg({'线上总额':np.median } )
    df_onDay_med.rename( columns= {'线上总额':'线上总额中位数'},inplace=True )
    ret_xs = pd.merge(ret_xs,df_onDay_med, on=['city_id'] ) 

    # 异常指标计算
    ret_xs['接驾异常'] = ret_xs.apply( exc_j, args=(take_driver_num, ) , axis=1  )
    ret_xs['服务异常'] =ret_xs.apply( exc_fw, args=(service_num,) , axis =1) 
    ret_xs[['间隔分钟','间隔里程']] = ret_xs[['间隔分钟','间隔里程']].astype(float)
    ret_xs['两单间隔异常'] = ret_xs.apply(exc_ldjg , args =(order_interval_num , ) ,axis =1 )
    ret_xs['多次握手异常'] = ret_xs.apply(exc_dcws, axis =1)
    
    #根据金额调整评分金额大于中位数：10倍+0.2， 2倍-0.4，大于中位数0.2，小于中位数则0 func_money
    ret_xs['金额异常']=ret_xs.apply(func_money ,axis =1)
    ret_xs['订单异常']=(ret_xs['接驾异常']+ret_xs['服务异常'] + ret_xs['两单间隔异常']+ret_xs['多次握手异常']+ret_xs['金额异常'] )* args_value
    
    return ret_xs




def Online_order_handle(order_online,df_drInfo, passenger_info, df_lx):
    # 整合司机异常
    order_online = pd.merge(order_online ,df_drInfo[['driver_id','司机异常']], how = 'left',on = ['driver_id'] )
    # 整合乘客异常
    order_online = pd.merge(order_online, passenger_info[['乘客异常','pay_card_no']] ,how='left', on=['pay_card_no'] )
    
    # 司机异常，乘客异常，进一步调整
    order_online['司机异常'] = order_online['司机异常'].fillna(0)
    order_online['乘客异常'] = order_online['乘客异常'].fillna(0)

    # 风险评分最终统计, 处理最终结果可能为负值的问题
    order_online['风险评分'] = order_online['订单异常'] + order_online['乘客异常'] + order_online['司机异常']
    order_online['np_Max0'] =0  
    order_online['风险评分'] = order_online[['风险评分','np_Max0']].apply(np.max, axis=1)
    order_online.drop(['np_Max0'],axis=1,inplace=True)
     
    # 整合司机拉新
    order_online= pd.merge(order_online , df_lx[['driver_id','passenger_id','status']], how='left', left_on=['driver_id','booking_user_id']  ,right_on=['driver_id','passenger_id'] )
      
    return order_online



def Func_new(ol_handle):
    # 调整风险评分, 根据金额异常等数据， 调整最终线上订单结果
    print('--- 调整风险评分 ---')
    # 根据拉新调整 （拉新且握手频次为1， 减去0.5）
    ol_handle['调整评分'] = ol_handle.apply(ret_newScore, axis =1) 
    ol_handle.drop(['passenger_id'],axis=1, inplace=True)
    return ol_handle




def Ret_table(ret_xs,df_fkDr):
    # 处理结果表
    print("--- 生成结果表 ---")
    ret_f = ret_xs.groupby(['city_id','driver_id' ]).size().reset_index()
    ret_f.rename(columns={0:'线上订单'},inplace=True)  

    # 处理风控订单num
    ret_f1= ret_xs[ret_xs['调整评分'] > 0.39999 ][['city_id','driver_id','调整评分']] 
    ret_f1 = ret_f1.groupby(['city_id','driver_id']).size().reset_index()
    ret_f1.rename(columns={0:'风控订单'} , inplace=True)
    ret_fr= pd.merge(ret_f, ret_f1, how='left', on=['city_id','driver_id'])
    ret_fr['风控订单']=ret_fr['风控订单'].fillna(0)  # 修改1

    # 处理remark
    df_fkDr2= df_fkDr[['user_id','remark']].drop_duplicates()
    ret_fr=pd.merge(ret_fr , df_fkDr2, how = 'left',left_on=['driver_id'] , right_on = ['user_id'])# 关联remark
    ret_fr =ret_fr.drop('user_id',axis=1)

    # 处理非拉新订单数据
    ret_xs['status']  = ret_xs['status'].fillna(0)
    ret_fr_flx = ret_xs[ret_xs['status']<3].groupby(['driver_id','city_id']).size().reset_index().rename(columns={0:'非拉新订单'})
    ret_fr = pd.merge(ret_fr, ret_fr_flx,how='left', on=['driver_id','city_id'])
    ret_fr['风控占比'] = round(ret_fr['风控订单']/ret_fr['线上订单'] ,5)
    return ret_fr



def Run_risk_info():

    # 设置保存路径
    print("===风控新规则处理===")

    psy = Psyco_handle()  # 风控库
     
    
    # 加载参数(数据指标)
    take_driver_num = 0.2  # 订单异常之 接驾异常参数  
    service_num = 0.2  # 订单异常之 服务常参数  
    order_interval_num = 0.2  # 订单异常之 两单间隔参数
    driver_exception_value = 0.35   # 司机异常系数
    args_value = 0.5    # 订单异常数值一级
    passenger_value = 0.15   # 乘客异常数值

    # 加载时间列表
    t_d = Date_list().timedlta(1)
    t_d = datetime.datetime.strftime(t_d, '%Y-%m-%d')
    t1= time.time()
	
        
    # 司机--乘客异常分析
    df_fkDr = Risk_record( t_d, psy )  # 1风控司机记录
    t101= time.time()
    
    df_drInfo = Df_drInfo(t_d, psy)    # 2司机信息表，司机异常计算
    t102= time.time()

    df_lx = Df_lx(t_d, psy)      # 3司机拉新
    t103= time.time()
    
    passenger_info= Passenger_info(t_d, psy)     # 4乘客异常
    t104= time.time()
    
 
    
    # 订单异常分析
    fk_s_d = Fk_seven_data(t_d,psy )    # 5风控七日订单数据
    t105= time.time()
    
    order_online = Order_online(t_d, psy ,fk_s_d ) # 线上订单数据
    t106= time.time()

    online_order_handle = Online_order_handle(order_online,df_drInfo,passenger_info,df_lx)  # 线上订单整合

    func_new = Func_new(online_order_handle)  # 评分调整
        

    ret_table = Ret_table(func_new,df_fkDr)  # 6结果表生成
    print("司机信息--%.2f; 司机拉新--%.2f; 乘客异常--%.2f;  风控七日--%.2f; 线上订单--%.2f; "   %( (t102-t101) , (t103-t102),(t104-t103),(t105-t104),(t106-t105))  )
    
    # 保存数据
    print("开始保存所有文件,请稍候...")
    df_drInfo['t_date'] = t_d 
    psy.data_s(df_drInfo, 't_risk_driver_info' )  # 1 司机信息表
    
    passenger_info['t_date'] = t_d
    psy.data_s(passenger_info, 't_risk_passenger_info') # 2   乘客信息表
    
    # psy.data_s(fk_s_d, 't_risk_seven_order')  3.0   七天风控
    func_new['t_date'] = t_d
    psy.data_s(func_new, 't_risk_online_order')  # 3 线上订单表

    ret_table['t_date'] = t_d
    psy.data_s(ret_table, 't_risk_result')  # 4  风控结果表
    
    t2 = time.time()
    
    
    
    print("fk--->: %.2f!" %(t2-t1))




if __name__ == '__main__':
    # t_d = '2018-02-28'
    # t_d = input("请输入风控日期:")
    # 设置保存路径
    print("===风控新规则处理===")
    

    # 加载参数(连接实例化)
    #print("正在加载参数中...")
    psy = Psyco_handle()  # 风控库
     
    
    # 加载参数(数据指标)
    take_driver_num = 0.2  # 订单异常之 接驾异常参数  
    service_num = 0.2  # 订单异常之 服务常参数  
    order_interval_num = 0.2  # 订单异常之 两单间隔参数
    driver_exception_value = 0.35   # 司机异常系数
    args_value = 0.5    # 订单异常数值一级
    passenger_value = 0.15   # 乘客异常数值

    # 加载时间列表
    t_dlist = ['2018-07-13', '2018-07-17','2018-07-18']
    t1= time.time()
	
    
    for  t_d in t_dlist:
    # 司机--乘客异常分析
        df_fkDr = Risk_record( t_d, psy )  # 1风控司机记录
        t101= time.time()
        
        df_drInfo = Df_drInfo(t_d, psy)    # 2司机信息表，司机异常计算
        t102= time.time()

        df_lx = Df_lx(t_d, psy)      # 3司机拉新
        t103= time.time()
        
        passenger_info= Passenger_info(t_d, psy)     # 4乘客异常
        t104= time.time()
        
     
        
        # 订单异常分析
        fk_s_d = Fk_seven_data(t_d,psy )    # 5风控七日订单数据
        t105= time.time()
        

        
        order_online = Order_online(t_d, psy ,fk_s_d) # 线上订单数据
        t106= time.time()

        online_order_handle = Online_order_handle(order_online,df_drInfo,passenger_info,df_lx)  # 线上订单整合

        func_new = Func_new(online_order_handle)  # 评分调整
            

        ret_table = Ret_table(func_new,df_fkDr)  # 6结果表生成
        print("司机信息--%.2f; 司机拉新--%.2f; 乘客异常--%.2f;  风控七日--%.2f; 线上订单--%.2f; "   %( (t102-t101) , (t103-t102),(t104-t103),(t105-t104),(t106-t105))  )
        
        # 保存数据
        print("开始保存所有文件,请稍候...")
        df_drInfo['t_date'] = t_d 
        psy.data_s(df_drInfo, 't_risk_driver_info' )  # 1 司机信息表
        
        passenger_info['t_date'] = t_d
        psy.data_s(passenger_info, 't_risk_passenger_info') # 2   乘客信息表
        
        # psy.data_s(fk_s_d, 't_risk_seven_order')  3.0   七天风控
        func_new['t_date'] = t_d
        psy.data_s(func_new, 't_risk_online_order')  # 3 线上订单表

        ret_table['t_date'] = t_d
        psy.data_s(ret_table, 't_risk_result')  # 4  风控结果表
    
    t2 = time.time()
    
    
    
    print("fk--->: %.2f!" %(t2-t1))


#over =input("over!")



