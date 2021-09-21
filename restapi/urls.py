from django.urls import path, re_path
from . import views
from rest_framework.authtoken.views import obtain_auth_token

from django.conf.urls import url

# app_name ='restapi'

urlpatterns = [
    path("order/", views.OrderPage.as_view(), name="order"),
    path("profile/", views.ProfilePage.as_view(), name="profile"),
    path("address/", views.AddressV.as_view(), name="address"),
    # path("profilep/", views.ProfilePostV.as_view(), name="profilef"),
    # ========== THIS IS HOME PAGE ==========
    url(r"^hm/", views.HomePage.as_view()),
    path("", views.HomePage.as_view(), name="home"),
    path("h/", views.HomeSec.as_view(), name="hsec"),
    path("reg/", views.DataGet.as_view(), name="getData"),
    # ==========POST REQUEST FOR ==================
    # path('login/', obtain_auth_token),
    path("login/", views.login, name="Login"),
    path("pm/", views.PostCartm, name="cartm"),
    path("crusr", views.PostRegister.as_view(), name="postdata"),
    path("crcart/", views.PostCart.as_view(), name="postcart"),
    path("crlike/", views.PostLike.as_view(), name="postlike"),
    path("crnoti/", views.PostNoti.as_view(), name="postnoti"),
    # ============ GET REQUEST FOR ALL ===========================
    path("p/", views.AllProduct.as_view(), name="product"),
    path("cart/", views.GetCart.as_view(), name="cart"),
    path("like/", views.GetLike.as_view(), name="like"),
    path("noti/", views.GetNoti.as_view(), name="noti"),
    # ================DELETE DATA ===============
    path("delcart/", views.DeleteCart.as_view(), name="delcart"),
    path("delnoti/", views.DeleteNoti.as_view(), name="delnoti"),
    path("dellike/", views.DeleteLike.as_view(), name="dellike"),
    path("search/", views.SrchProduct.as_view(), name="searchbar"),
    path("ser/", views.Srh.as_view(), name="ser"),
    # url(r'^$',views.SrchProduct.as_view(),name='searchbar'),
    # re_path('^ser/(?P<fullname>.+)/$', views.SrchProduct.as_view(),name='searchb')
]
