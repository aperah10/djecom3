from django.contrib import admin
from .models import * 

# Myorder
@admin.register(AllOrder)
class OrderAdmin(admin.ModelAdmin):
  list_display=('id','status', 'product','quantity','user')
 

   
# PRDOCUT IN CART
@admin.register(CancelOrder)
class CancelAdmin(admin.ModelAdmin):
  list_display=('id','status', 'product','quantity','user')

# LIKE
@admin.register(AllDataNotification)
class AllDataNotiAdmin(admin.ModelAdmin):
  list_display=('id','orderkey','user','addresskey') 


# NOTIFICATIONS
@admin.register(NotificationOrder)
class OrderNotificationAdmin(admin.ModelAdmin):
  list_display=('id','product','sender','status','date','is_seen','txt')