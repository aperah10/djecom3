from django.contrib import admin
from .models import * 
# Register your models here.

# PRODUCT
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
   list_display=('id','uplod','title','description','sales_price','our_price','discount_price','category','date','stock','pic','offers')
 

   
# PRDOCUT IN CART
@admin.register(ProductInCart)
class ProductInCartAdmin(admin.ModelAdmin):
  list_display=('id','product','customer_cart','quantity','created_on')

# LIKE
@admin.register(Like)
class LikeAdmin(admin.ModelAdmin):
  list_display=('id','product','user','cr_date') 

# Saveforlater
@admin.register(ProductInSave)
class ProSaveAdmin(admin.ModelAdmin):
  list_display=('id','product','cart_by','customer_cart','quantity',)

# NOTIFICATIONS
@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
  list_display=('id','product', 'user','sender','noti_type','date','is_seen','txt')