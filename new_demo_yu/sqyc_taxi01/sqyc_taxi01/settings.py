"""
Django settings for sqyc_taxi01 project.

Generated by 'django-admin startproject' using Django 1.8.2.

For more information on this file, see
https://docs.djangoproject.com/en/1.8/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.8/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
import  re


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.8/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '09-@_l1%+k9+#%c#1f3u^$5@*jx7wc2y#h5457@m9sppes1w69'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True
# DEBUG = False
ALLOWED_HOSTS = ['*']


# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'sqyc_bi' , #  注册项目
    'django_crontab',
    'bi_echarts',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.security.SecurityMiddleware',
)

ROOT_URLCONF = 'sqyc_taxi01.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR,'templates')], #  设置模板路径， 在当前项目大根目录下
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'sqyc_taxi01.wsgi.application'

ehp = 'kl52jwer11ifj68kf06nrew'

str = 'Yuyx'


# Database
# https://docs.djangoproject.com/en/1.8/ref/settings/#databases



DATABASES = {
    'default': {
        #'ENGINE': 'django.db.backends.sqlite3',
        'ENGINE': 'django.db.backends.postgresql_psycopg2',  # mysql; postgresql_psycopg2

        'NAME': "taxidb",   # mysql: sqyc_db, pg: taxidb
        'USER': 'taxiuser',
        'PASSWORD': 'taxiuser',
        'HOST':'localhost',
        'PORT':5432,     # mysql:3306 ,  pg: 5432
    }
}



#
# DATABASES = {
#       'default': {
#           #'ENGINE': 'django.db.backends.sqlite3',
#           'ENGINE': 'django.db.backends.postgresql_psycopg2',
#           'NAME': "taxidb",
#           'USER': 'taxiuser',
#           'PASSWORD': 'taxiuser',
#           'HOST':'localhost',
#           'PORT':5432
#       }
#   }



# Internationalization
# https://docs.djangoproject.com/en/1.8/topics/i18n/

LANGUAGE_CODE = 'zh-Hans'

TIME_ZONE = 'Asia/Shanghai'

USE_I18N = True

USE_L10N = True

USE_TZ = True



EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.01zhuanche.com'
EMAIL_PORT = 25

EMAIL_HOST_USER = 'yuweihong@01zhuanche.com'
EMAIL_HOST_PASSWORD = ''.join(re.findall('\d+', ehp) )+str
EMAIL_FROM = 'yuweihong'


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.8/howto/static-files/

STATIC_URL = '/static/'
STATICFILES_DIRS = [ os.path.join(BASE_DIR,'static'), ] # 设置静态文件物理目录

STATIC_ROOT = "/var/www/sqyc/c_static2/"

CRONJOBS = [
    ('30 08 * * *', 'sqyc_bi.tests.demo1'),
    ('30 12 * * *', 'sqyc_bi.tests.R_driver_num' ) ,
    ('00 13 * * *', 'sqyc_bi.tests.demo3' ) ,


]






