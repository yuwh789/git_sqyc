from django.contrib import admin
from bi_echarts.models import  *
# Register your models here.

class func_commentAdmin(admin.ModelAdmin):
    list_per_page = 20  # 页码
    list_display = ['title', 'func_name', 'comment']
    list_filter = ['title']


admin.site.register(func_comment, func_commentAdmin)