from django.db import models
from accounts.models import CustomUser
from django.urls import reverse
import uuid 




# ADD PRODUCT 
#  ---------------------ADD PRODUCT --------------------------
Cat=( ('Clothes','Clothes') ,('Mobile','Mobile'),('Beauty','Beauty'),('Grocery','Grocery'))

class Product(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title=models.CharField(max_length=100)
    description=models.CharField(max_length=300) 
    sales_price=models.FloatField()
    discount_price=models.FloatField()
    our_price=models.FloatField(blank=True,null=True ,default=0)
    category=models.CharField(choices=Cat,max_length=200)
    date=models.DateTimeField(auto_now_add=True)
    stock=models.PositiveIntegerField()
    pic=models.ImageField(upload_to='ProdcutImg',blank=True)
    offers=models.IntegerField(default=1,null=True,blank=True) 
    uplod=models.ForeignKey(to=CustomUser,on_delete=models.CASCADE,null=True,blank=True) 
 

    def get_absolute_url(self):
        return reverse('product', kwargs={'pk':self.pk}) 
        
    def __str__(self):
       return self.title  



# PRODUCT IN CART
#  --------------------- --PRODUCT IN CART --------------------------
class ProductInCart(models.Model):
    
    class Meta:
        unique_together=(('customer_cart'),('product')) 
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    product=models.ForeignKey(Product,on_delete=models.CASCADE)
    customer_cart=models.ForeignKey(CustomUser,on_delete=models.CASCADE)
    quantity=models.PositiveIntegerField(default=1)
    created_on=models.DateTimeField(auto_now_add=True)
    
    # def __str__(self):
    #     return str(self.id) 
    def __str__(self):
        return f"User={self.product.uplod}|Quantity={self.quantity}"



#  --------------------- PRODUCT IN SAVE  --------------------------
# PRODUCT IN Savefor Later 
class ProductInSave(models.Model):
    
    class Meta:
        unique_together=(('customer_cart'),('product'),('cart_by')) 

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    product=models.ForeignKey(Product,on_delete=models.CASCADE) 
    cart_by=models.ForeignKey(to=ProductInCart,on_delete=models.CASCADE,null=True,blank=True)
    customer_cart=models.ForeignKey(CustomUser,on_delete=models.CASCADE ,)
    quantity=models.PositiveIntegerField(default=1)
    created_on=models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return str(self.id)  


#  --------------------- PRODUCT LIKE --------------------------
# PRODUCT LIKE 
class Like(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    product=models.ForeignKey(to=Product,on_delete=models.CASCADE)
    user=models.ForeignKey(to=CustomUser,on_delete=models.CASCADE,null=True,blank=True)
    cr_date=models.DateTimeField(auto_now_add=True)



#  --------------------- PRODUCT NOTIFICATION --------------------------
# NOTIFICATIONS 
Noti_Type=(('Like','Like'),('addtocart','addtocart'),('save for later','save for later')) 
class Notification(models.Model):
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    product=models.ForeignKey(to=Product,on_delete=models.CASCADE,null=True,blank=True) 
    sender=models.ForeignKey(to=CustomUser,on_delete=models.CASCADE,related_name='sendernoti')
    user=models.ForeignKey(to=CustomUser,on_delete=models.CASCADE,related_name='receviernoti') 
    noti_type=models.CharField(choices=Noti_Type,max_length=50)
    txt=models.CharField(max_length=100)
    date=models.DateTimeField(auto_now_add=True)
    is_seen=models.BooleanField(default=False) 
