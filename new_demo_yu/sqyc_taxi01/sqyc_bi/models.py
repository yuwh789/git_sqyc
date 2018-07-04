from django.db import models
from sqyc_bi.untils.get_hash import get_hash
from django.shortcuts import  redirect



class UserManager(models.Model):
    '''用户账户管理器类'''
    def add_one_manager(self, uname, passwd, adminpasswd):
        '''添加一个用户注册信息'''

        if adminpasswd == 'helloworld':
            user = user_account()
            user.user_name = uname
            user.password = get_hash(passwd)
            user.save()
            return  user
        else:
            return "Wrong"


    def get_one_manager(self,uname,passwd=None):
        '''根据用户名和密码查询信息'''
        # try:
        #     if passwd is None:
        #         user  = self.get(uname=uname)
        pass




# Create your models here.
class sqyc_table(models.Model):
    # 城市id
    city_id = models.IntegerField()
    # 城市name
    city_name = models.CharField(max_length=20)

    # 司机id
    driver_id = models.IntegerField()
    # 司机name
    driver_name = models.CharField(max_length=20)

    # 司机电话
    driver_phone = models.CharField(max_length=12)

    # 司机所属公司
    company_name = models.CharField(max_length=100)

    # 更新时间
    #update_date = models.DateField()

    pass


class user_account(models.Model):
    user_name= models.CharField(max_length=20)
    password = models.CharField(max_length= 40)
    phone = models.CharField( max_length =30 )
    comment = models.CharField(max_length=50)

    objects = UserManager()

class t_driver_order_num(models.Model):
    create_date = models.DateField()
    order_status = models.CharField(max_length=10)
    recmd_status = models.CharField(max_length=10)
    one_num = models.CharField(max_length=10)
    two_num = models.CharField(max_length=10)
    three_num = models.CharField(max_length=10)
    four_num = models.CharField(max_length=10)
    five_seven_num =models.CharField(max_length=10)
    eight_ten_num = models.CharField(max_length=10)
    gt_eleven_num = models.CharField(max_length=10)
    update_date = models.DateField(auto_now=True)

    class Meta:
        db_table='t_driver_order_num'




class t_experience(models.Model):
    '''乘客体验'''
    pass



class t_company_day_data(models.Model):
    '''分公司日报'''
    t_date = models.DateField()
        # models.date(max_length=20)
    city = models.CharField(max_length=30)
    city_id = models.IntegerField()
    driver_id = models.IntegerField()
    driver_name = models.CharField(max_length=30)
    driver_phone = models.CharField(max_length=30)
    taxi_company_id = models.IntegerField()
    taxi_company_name = models.CharField(max_length=30)
    com_cnt=models.IntegerField()
    reward_punish_money = models.FloatField()
    plate_number = models.CharField(max_length=30)
    id_number = models.CharField(max_length=30)
    total_online_minute = models.IntegerField()
    update_date = models.DateField(auto_now=False)

    class Meta:
        db_table = 't_company_day_data'
    pass











