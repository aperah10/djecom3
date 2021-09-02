from django.urls import path
from . import views 

urlpatterns =[
   path('',views.CrProduct.as_view(success_url="/addproduct/"),name='addproduct'),
   path('productshow/<int:pk>/',views.ProductShow.as_view(),name='ProductShow'),
   path('addtocart/',views.ProductInC,name='pnc'),
   path('cart/',views.Show_Cart,name='Cart'),
   
] 