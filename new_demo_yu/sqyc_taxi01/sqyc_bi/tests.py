from django.test import TestCase
import time , datetime
from sqyc_bi.my_test_day import *
from sqyc_bi.data_tools import  *
from sqyc_bi.num_amount_score import *
from sqyc_bi.run_ser_pas import *
from sqyc_bi.pas_add import *

def demo1():
    run_company_day()
    print("run_company_day over!")

    time.sleep(1)
    Run_num_amount_score(44)
    print('run_num_amount_score over!')

    time.sleep(1)
    run_pas_add()
    print("run_pas_add over!")


def R_driver_num():
    Run_driver_num()
    print("run_driver_num over!")

    time.sleep(2)
    Run_hb_tb()
    print("run_hb_tb over!")
    
    time.sleep(2)
    Run_risk()
    print('run_risk over!')

def demo3():
    run_ser_pas()
    print('run_ser_pas over!')

if __name__=="__main__":
    print("start")
    demo1()
    print("end!")


