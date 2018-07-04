from django.test import TestCase
import time
from sqyc_bi.my_test_day import * 
# Create your tests here.



def demo1():
	run_company_day()
	#est_cany_day('2018-05-01','94','天鹅')

def R_driver_num():
	Run_driver_num()
	time.sleep(2)
	Run_hb_tb()	


if __name__=="__main__":
	print("start")
	demo1()
	print("end!")


