from django.contrib import admin

# Register your models here.
from sqyc_bi.models import  *



class sqyc_tableAdmin(admin.ModelAdmin):
    list_per_page =  20  # 页码

    list_display = ['city_id','city_name','driver_name','company_name']

    list_filter = ['driver_name']

    search_fields = ['driver_name']



class user_accountAdmin(admin.ModelAdmin):
    list_per_page =  20  # 页码
    list_display = ['user_name','password','phone']
    list_filter = ['user_name']
    search_fields = ['phone']


class t_driver_order_numAdmin(admin.ModelAdmin):
    list_per_page = 20
    list_display = ['create_date','order_status','recmd_status','one_num','two_num','three_num','four_num']
    list_filter = ['create_date']
    search_fields = ['create_date']


admin.site.register(sqyc_table,sqyc_tableAdmin)

admin.site.register(user_account,user_accountAdmin)

admin.site.register(t_driver_order_num,t_driver_order_numAdmin)