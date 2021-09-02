from django.db import models
import uuid 
from accounts.models import * 
from product.models import *  

# Create your models here.

# ------------------ORDER MODEL ------------------------------ 
State_Types=( ('Pending','Pending'),('Accept','Accept'),('Decline','Decline'),('Dispatch','Dispatch'),('Shipment','Shipment'),
('Arrives at','Arrives at'), ('Complete','Complete'))   



# ORDER BASE CLASS 
class BaseOrder(models.Model):
    amount = models.PositiveIntegerField(default=100)
    status = models.CharField(max_length=100 , choices = State_Types , default="Pending")
    date = models.DateTimeField(auto_now_add=True)
    quantity = models.PositiveIntegerField(default=1) 
    Location =models.CharField(max_length=100,default=100)

    def __str__(self):
        return str(self.id)   
    class Meta:
        abstract=True

class AllOrder(BaseOrder):
    id =models.UUIDField(primary_key=True,editable=False,default=uuid.uuid4,)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE,)

# CANCEL ORDER 
class CancelOrder(BaseOrder):
    id =models.UUIDField(primary_key=True,) 
    user = models.ForeignKey(AllOrder, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE )

# Success ORDER
class SuccessOrder(BaseOrder):
    id =models.UUIDField(primary_key=True,) 
    user = models.ForeignKey(AllOrder, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE )

# -------------- NOTIFICATIONS -----------------------------

class NotificationOrder(BaseOrder):
    product=models.ForeignKey(to=Product,on_delete=models.CASCADE,null=True,blank=True,related_name='alldatanoti') 
    sender=models.ForeignKey(to=CustomUser,on_delete=models.CASCADE,related_name='sendernotifororder')
    user=models.ForeignKey(to=CustomUser,on_delete=models.CASCADE,related_name='receviernotifororder') 
    txt=models.CharField(max_length=100,null=True,blank=True)
    is_seen=models.BooleanField(default=False)   


# ONE NOIFICATION FOR ALL DATA OF USER 
class AllDataNotification(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user=models.ForeignKey(to=CustomUser,on_delete=models.CASCADE,related_name='usersnotications')
    orderkey=models.ForeignKey(to=AllOrder,on_delete=models.CASCADE,related_name='orderbox')
    addresskey=models.ForeignKey(to=Address,on_delete=models.CASCADE,related_name='address')