from django.contrib import admin
from django.urls import path,include  
from django.conf import settings 
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('acc/',include('accounts.urls')),
    path('user/',include('customer.urls')),
    path('prod/',include('product.urls')),
    path('',include('restapi.urls')),

] + static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
