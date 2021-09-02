from .base import *

with open(os.path.join(BASE_DIR,'secret.txt')) as f :
    SECRET_KEY= f.read().strip()

DEBUG = False 

ALLOWED_HOSTS = ["djecomf.herokuapp.com",'127.0.0.1',] 



INSTALLED_APPS += [
    'rest_framework',
    'rest_framework.authtoken',
    'django_filters',
    'accounts',
    'customer',
    'product',
    'restapi',
    'corsheaders',
]


 # ---------------------------------------------------------------------------- #
 #                              !DATABASE SETTINGS                              #
 # ---------------------------------------------------------------------------- #
import dj_database_url 
db_from_env = dj_database_url.config(conn_max_age=600)
DATABASES ['default'].update(db_from_env)