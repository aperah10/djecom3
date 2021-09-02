from .base import * 

 
# SECRET_KEY = 'django-insecure-0-5dx27s6!)t6#rk70gmkdc1lspk_8gsg(kb-^d#wla4o&_g%_'
with open(os.path.join(BASE_DIR,'secret.txt')) as f :
    SECRET_KEY= f.read().strip()

DEBUG = True 

ALLOWED_HOSTS = ['127.0.0.1',] 



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