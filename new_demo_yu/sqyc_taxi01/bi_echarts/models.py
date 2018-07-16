from django.db import models

# Create your models here.

class func_comment(models.Model):
    '''title, func_name, comment'''
    title = models.CharField(max_length=20)
    func_name= models.CharField(max_length=20)
    comment = models.CharField(max_length=40)