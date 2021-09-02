from django import forms 
from .models import * 


# PRODUCT FORM
class ProductForm(forms.ModelForm):
    class Meta:
        model=Product
        fields=['title','description','sales_price','discount_price','stock','category','pic']  
    
   