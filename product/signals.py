from django.dispatch.dispatcher import receiver
from django.db.models.signals import post_save 
from .models import * 

# addtocart 
@receiver(post_save,sender=ProductInCart)
def add_to_cart(sender,instance,created,*arg,**kwargs): 
    like=instance 
    product=like.product  
    sender=like.customer_cart 
    # print("add in  LIKE  " ,like)
    # print("add in  product  " ,product) 
    # print("add in  sender " ,sender)
    # if created:
    notifty=Notification(product=product,sender=like.customer_cart,user=product.uplod,noti_type='addtocart') 
    notifty.save()
    # print("add in  add to cart  ") 

Like 
@receiver(post_save,sender=Like)
def user_like(sender,instance, created,*arg,**kwargs): 
    like=instance 
    product=like.product 
    sender=like.user 
    if created :
     notifty=Notification(product=product,sender=sender,user=product.uplod,noti_type='Like')  
     notifty.save()
    #  print("add in  Like ") 

# # # SAVEFOR LATER 
# @receiver(post_save,sender=ProductInCart) 
# @receiver(post_save,sender=Product)
# def save_for_later(sender,instance,created,*arg,**kwargs):  
#     print('------------------------------------------------------')
#     print('instance ', type(instance)) 
#     print('sender ', sender)
#     if sender == Product: 
#       notify= ProductInSave(product=instance,customer_cart=instance.customer_cart, quantity=instance.quantity,) 
#       notify.save()
#       print("add in save for later ") 
    
#     if sender == ProductInCart: 
#         notify= ProductInSave(cart_by=instance,customer_cart=instance.customer_cart, quantity=instance.quantity,) 
#         notify.save() 
#         met =ProductInCart.objects.filter(customer_cart=instance.customer_cart,cart_by=instance).delete()
#         print("add in save for later from addtocart  ") 