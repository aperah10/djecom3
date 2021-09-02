from django.urls import path
from . import views 
from django.views.generic.base import RedirectView

urlpatterns =[
   
    path('',views.Register.as_view(),name='signup'),
    path('login/',views.LoginPage.as_view(),name='login'),
    path('logout/',views.LogoutPage,name='logout'),
    path('cusprofile/<uuid:pk>/',views.Profile.as_view(),name='profile'),
    path('address/<uuid:pk>/',views.AddAddress.as_view(),name='address'),
    path('showaddress/<uuid:pk>/',views.ShowAddress.as_view(),name='showaddress'),
    path('upaddress/<uuid:pk>/',views.UpAddress.as_view(),name='upaddress'),
    path('deladdress/<uuid:pk>/',views.DelAddress,name='deladdress'),
    
]