from sturnus.settings import *

DEBUG = True

ADMINS = (
    ('Justin Kiggins', 'justin.kiggins@gmail.com'),
)

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': 'sturnus.db',
    }
}