from django.test import TestCase
import time
from sqyc_bi.my_test_day import * 
# Create your tests here.
# TAB


def demo1():
	print("run_company_day")
	run_company_day()
	#est_cany_day('2018-05-01','94','天鹅')
	time.sleep(3)
	print("run_risk")
	Run_risk()

def R_driver_num():
	Run_driver_num()
	print("run_driver_num")
	time.sleep(2)
	Run_hb_tb()
	print("run_hb_tb")


if __name__=="__main__":
	print("start")
	demo1()
	print("end!")


