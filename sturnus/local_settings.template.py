from sturnus.settings import *

DEBUG = False

ADMINS += ('Name', 'name@example.com')

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2', # must be a postgres database for django_neo
        'NAME': 'db_name',
        'USER': 'db_user',
        'PASSWORD': 'db_user_pass',
        'HOST': '', # Set to empty string for localhost.
        'PORT': '5432', # 5432 is default postgres port
    }
}

STATIC_ROOT = '/home/user/www/sturnus/static/'
