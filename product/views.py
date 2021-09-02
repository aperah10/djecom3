from django.shortcuts import redirect, render
from django.views import View
from django.views.generic.base import TemplateView 
from django.views.generic.edit import CreateView
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required


# MY IMPORT 
from .models import * 
from .forms import * 



# CREATE POST
# @method_decorator(login_required,name='dispatch') 
class CrProduct(CreateView):
    model=Product
    fields=['title','description','sales_price','discount_price','stock','category','pic','offers']
    template_name='product/product.html'
    
    def form_valid(self,form): 
       
        self.object=form.save()
        self.object.uplod=self.request.user
        self.object.save()


# PRODCUT SHOW WITH DETAILS  
class ProductShow(TemplateView):
    def get(self,request,pk=None): 
        
        prod=Product.objects.get(uplod=pk)

        context={'product':prod}
        return render(request,'product/ProductS.html',context)



# PRODCUT IN ADD CART  
def ProductInC(request):
    user=request.user 
    prod_id=request.GET.get('product_id')
    prod=Product.objects.get(pk=prod_id)  
    print('product :- ',prod)
    # if ProductInCart.objects.filter(Q(customer_cart__iexact=user) & Q(product__iexact=prod)).exists:
    #     return HttpResponse('you already add this product')
    ProductInCart.objects.create(customer_cart=user,product=prod)
    return redirect('Cart')  



# PRODCUT CART SHOW WITH DETAILS  
def Show_Cart(request):
    user=request.user
    prod_cart=ProductInCart.objects.filter(customer_cart=user) 
    
    print("---------------------")
    print(prod_cart)
    amount=0.0
    shiping_amount=70.0
    total_amount=0.0
    cart_product=[p for p in ProductInCart.objects.all() if p.customer_cart==user]
    print(cart_product)
    if cart_product:
        for r in cart_product:
           temamount=(r.quantity* r.product.discount_price)
           amount += temamount
           total_amount=amount + shiping_amount 
        return render(request,'product/ProductInCart.html',
            {'mango':prod_cart,'tom':total_amount,'ammount':amount,'shiping':shiping_amount})

    else:
        return render(request,'product/PEmpty.html')






