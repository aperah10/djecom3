from django.shortcuts import render
from rest_framework.generics import (
    ListAPIView,
    CreateAPIView,
    RetrieveAPIView,
    ListCreateAPIView,
    RetrieveUpdateDestroyAPIView,
)
from rest_framework.authentication import BaseAuthentication
from rest_framework.permissions import (
    IsAuthenticated,
    IsAuthenticatedOrReadOnly,
    AllowAny,
)
from rest_framework.authentication import TokenAuthentication
from rest_framework.views import APIView
from django.db.models import Q
from rest_framework.response import Response
from django.contrib.auth.hashers import make_password

from django.views.generic import TemplateView
from rest_framework.status import HTTP_400_BAD_REQUEST, HTTP_404_NOT_FOUND, HTTP_200_OK
from django.contrib.auth import authenticate, login, logout
from django.views.decorators.csrf import csrf_exempt
from rest_framework.authtoken.models import Token
from rest_framework import generics, permissions
from rest_framework.decorators import (
    api_view,
    permission_classes,
    authentication_classes,
)

from rest_framework.filters import SearchFilter
from django_filters.rest_framework import DjangoFilterBackend


# MY IMPORTS FOR ALL FILES
from accounts.models import *
from product.models import *
from .serializer import *


# Create your views here.
#  HOME PAGE
class HomePage(TemplateView):
    template_name = "restapi/Home.html"


class HomeSec(TemplateView):
    template_name = "restapi/HomeSec.html"


# GET DATA API
class DataGet(ListAPIView):
    # permission_classes=[IsAuthenticated,]
    queryset = ProductInCart.objects.all()
    serializer_class = CartSer


# # UPDATE AND DESTROY AND GET  USER DATA


# POST DATA FOR CREATE USER
class PostRegister(APIView):
    def post(self, request, format=None):
        data = request.data
        # if CustomUser.objects.filter(phone__exact=data.get('phone')):
        #     return Response({"stateCode": 201, "msg": "User Exits"}, 201)
        # if CustomUser.objects.filter(email__exact=data.get('email')):
        #     return Response({"stateCode": 202, "msg": "User enn"}, 201)
        new_user = {
            "fullname": data.get("fullname"),
            "phone": data.get("phone"),
            "email": data.get("email"),
            "password": make_password(data.get("password")),
        }
        # print(new_user)
        serializer = AccountsSeri(data=new_user)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            user = serializer.save()
            username = data.get("phone")
            raw_password = data.get("password")

            cur_user = authenticate(username=username, password=raw_password)

            token, _ = Token.objects.get_or_create(user=cur_user)
            return Response(
                {
                    "stateCode": 200,
                    "msg": "enter data",
                    "token": token.key,
                },
                200,
            )
        return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)


# =============================== LOGIN   =====================================
@csrf_exempt
@api_view(["POST"])
@permission_classes((AllowAny,))
def login(request):
    username = request.data.get("phone")
    password = request.data.get("password")
    # if username is None or password is None:
    #     return Response({'error': 'Please provide both username and password'},
    #                     status=HTTP_400_BAD_REQUEST)
    # user = authenticate(username=username, password=password)
    try:
        user = authenticate(
            username=CustomUser.objects.get(email__iexact=username), password=password
        )

    except:
        user = authenticate(username=username, password=password)

    if not user:
        return Response({"error": "Invalid Credentials"}, status=HTTP_404_NOT_FOUND)
    token, _ = Token.objects.get_or_create(user=user)
    return Response({"token": token.key}, status=HTTP_200_OK)


# ! POST METHOD
@csrf_exempt
@api_view(["POST"])
@permission_classes((IsAuthenticated,))
@authentication_classes((TokenAuthentication,))
def PostCartm(request):

    quan = request.data.get("quantity")
    prod = request.data.get("product")
    usr = request.user.id
    # usr = request.data.get("customer_cart")

    # print(
    #     "-----------------------------------------------------------------------------"
    # )

    # print("quantity:- ", quan)
    # print("prod:- ", prod)

    new_cart = {"quantity": quan, "product": prod, "customer_cart": str(usr)}
    # print(new_cart)

    # if ProductInCart.objects.filter(
    #     Q(customer_cart__exact=data.get("customer_cart"))
    #     & Q(product__exact=data.get("product"))
    # ):
    #     return Response({"stateCode": 201, "msg": "User Exits"}, 201)

    serializer = AddCartSer(data=new_cart)
    # print('this is data :-' ,data)

    print("this is seriallizer:- ", serializer)
    if serializer.is_valid(raise_exception=True):

        serializer.save()
        user = serializer.save()
        return Response(
            {
                "stateCode": 200,
                "msg": "enter data",
            }
        )

    return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)


# nrw cart post for check
# @csrf_exempt
class PostCart(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [
        TokenAuthentication,
    ]

    # queryset = ProductInCart.objects.all()
    # serializer_class=CartSer
    # @csrf_exempt
    def post(self, request):
        data = request.data
        # product_id = request.data['id']
        # product_obj = Product.objects.get(id=product_id)
        new_cart = {
            "quantity": data.get("quantity"),
            "product": data.get("product"),
            "customer_cart": str(request.user.id),
            # "customer_cart": data.get("customer_cart"),
        }

        if ProductInCart.objects.filter(
            Q(customer_cart__exact=request.user.id)
            & Q(product__exact=data.get("product"))
        ):
            return Response({"stateCode": 201, "msg": "User Exits"}, 201)

        serializer = AddCartSer(data=new_cart)
        # print('this is data :-' ,data)
        # print('this is seriallizer:- ',serializer)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            user = serializer.save()
            return Response(
                {
                    "stateCode": 200,
                    "msg": "enter data",
                }
            )
        return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)


# NEW LIKE  post for check
class PostLike(CreateAPIView):
    permission_classes = [IsAuthenticated]
    # authentication_classes = [TokenAuthentication, ]

    queryset = Like.objects.all()
    serializer_class = LikeSer


# NEW  NOTITFICATION  POST  FOR
class PostNoti(CreateAPIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [
        TokenAuthentication,
    ]

    queryset = Notification.objects.all()
    serializer_class = NotificationSer


# ---------------------------------------------------------------------------- #
#                                 ! GET METHOD                                 #
# ---------------------------------------------------------------------------- #

# ! PRODUCT SEARCH BAR
class SrchProduct(ListAPIView):
    queryset = Product.objects.all()
    serializer_class = AllProductSer
    search_fields = ["title", "description"]
    # queryset=CustomUser.objects.all()
    # serializer_class=AccountsSeri
    filter_backends = [DjangoFilterBackend, SearchFilter]
    # search_fields=['fullname', 'phone']


#     # ! this is used in Filter
#     # filter_backends = [DjangoFilterBackend]
#     # filterset_fields = ['title', 'description']


class Srh(ListAPIView):
    serializer_class = AccountsSeri

    def get_queryset(self):
        if self.request.method == "GET":
            queryset = CustomUser.objects.all()
            state_name = self.request.GET.get("q", None)
            if state_name is not None:
                queryset = queryset.filter(fullname=state_name)
            return queryset


#  =======================GET DATA  SECTION =================================
# SHOW ALL PRODUCT
class AllProduct(ListAPIView):

    queryset = Product.objects.all()
    serializer_class = AllProductSer


# CART FOR USER
class GetCart(APIView):
    permission_classes = [IsAuthenticated]
    # authentication_classes = [TokenAuthentication, ]

    def get(self, request):
        usr = request.user
        token = Token.objects.get(user=usr)
        print("GET Cart Request user", usr)
        print("GET Cart Request TOKEN", token)
        usr_cart = ProductInCart.objects.filter(customer_cart=usr)

        try:
            ser = CartSer(usr_cart, many=True)
            alldata = ser.data

        except:
            print("this is token reutest")
            alldata = ser.errors
        return Response(alldata)


# LIKE OF USER
class GetLike(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [
        TokenAuthentication,
    ]

    def get(self, request):
        usr = request.user
        print("GET LIKE Request user", usr)
        usr_like = Like.objects.filter(user=usr)

        try:

            ser = LikeSer(usr_like, many=True)
            alldata = ser.data

        except:
            alldata = ser.errors

        return Response(alldata)


# # MAKING NOTIFICATION
class GetNoti(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [
        TokenAuthentication,
    ]

    def get(self, request):
        usr = request.user
        noti = Notification.objects.filter(user=usr)

        try:

            ser = NotificationSer(noti, many=True)
            alldata = ser.data

        except:
            alldata = ser.errors

        return Response(alldata)


# ---------------------------------------------------------------------------- #
#                                ! DELETE METHOD                               #
# ---------------------------------------------------------------------------- #
# =========================DELETE =================


# !DELETE CART
class DeleteCart(APIView):
    permission_classes = [
        IsAuthenticated,
    ]
    authentication_classes = [
        TokenAuthentication,
    ]

    # @csrf_exempt
    def post(self, request):
        prod = request.data.get("product")
        # cus = str(request.data.get("customer_cart"))
        cus = request.user
        # print("product:- ", prod)
        # print("cus :- ", cus)

        try:
            if ProductInCart.objects.filter(
                Q(customer_cart=cus) & Q(product=prod)
            ).exists():
                pod = ProductInCart.objects.filter(
                    Q(customer_cart=cus) & Q(product=prod)
                )
                print(pod)
                pod.delete()
                res = {"error": False, "msg": "data delete"}
            else:
                res = {"error": True, "msg": " not have any data"}

        except:
            res = {"error": True}
        return Response(res)


# # DELETE FOR LIKE


class DeleteLike(APIView):
    permission_classes = [
        IsAuthenticated,
    ]
    authentication_classes = [
        TokenAuthentication,
    ]

    def post(self, request):
        prod = request.data["product"]
        cus = request.data["user"]

        try:
            if Like.objects.filter(Q(user=cus) & Q(product=prod)).exists():
                pod = Like.objects.filter(Q(user=cus) & Q(product=prod))
                print(pod)
                pod.delete()
                res = {"error": False, "msg": "data delete"}
            else:
                res = {"error": True, "msg": " not have any data"}

        except:
            res = {"error": True}
        return Response(res)


# DELETE FOR NOTITFICATION


class DeleteNoti(APIView):
    permission_classes = [
        IsAuthenticated,
    ]
    authentication_classes = [
        TokenAuthentication,
    ]

    def post(self, request):
        prod = request.data["product"]
        cus = request.data["user"]
        sender = request.data["sender"]

        try:
            if Notification.objects.filter(
                Q(Q(user=cus) & Q(product=prod)) & Q(Q(user=cus) & Q(sender=sender))
            ).exists():
                pod = Notification.objects.filter(
                    Q(Q(user=cus) & Q(product=prod)) & Q(Q(user=cus) & Q(sender=sender))
                )
                print(pod)
                pod.delete()
                res = {"error": False, "msg": "data delete"}
            else:
                res = {"error": True, "msg": " not have any data"}

        except:
            res = {"error": True}
        return Response(res)


# ---------------------------------------------------------------------------- #
#                     orc   PROFILE PAGE GET AND POST METHOD                     #
# ---------------------------------------------------------------------------- #
class ProfilePage(APIView):
    permission_classes = [
        IsAuthenticated,
    ]
    authentication_classes = [
        TokenAuthentication,
    ]

    # todo  GET METHOD
    def get(self, request):
        usr = request.user
        prof = Profile.objects.filter(uplod=usr)
        # prof = Profile.objects.filter(uplod="e1ff4d87-d9a6-4533-836a-0c640034b8eb")

        try:

            ser = ProfileSer(prof, many=True)
            alldata = ser.data

        except:
            alldata = ser.errors

        return Response(alldata)

    # orc PROFILE POST METHOD

    def post(self, request, pk=None):
        data = request.data
        idt = request.user.id
        # idt = request.data.get("id")

        cus = Profile.objects.get(pk=idt)
        # print("this is profile id ,:- ", idt)

        # print(cus)
        # product_obj = Product.objects.get(id=product_id)
        new_profile = {
            "fullname": data.get("fullname"),
            "email": data.get("email"),
            "gender": data.get("gender"),
            "pic": data.get("pic"),
        }

        # print(new_profile)
        serializer = PostProfileSer(cus, data=new_profile)

        # print(serializer)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            user = serializer.save()
            return Response(
                {
                    "stateCode": 200,
                    "msg": "enter data",
                }
            )
        return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)


# ---------------------------------------------------------------------------- #
#                   ! ADDRESS POST & GET  METHOD                                     #
# ---------------------------------------------------------------------------- #
class AddressV(APIView):

    # permission_classes = [
    #     IsAuthenticated,
    # ]
    # authentication_classes = [
    #     TokenAuthentication,
    # ]

    # todo  GET METHOD
    def get(self, request):
        usr = request.user
        addres = Address.objects.filter(uplod=usr)
        # addres = Address.objects.filter(uplod="e1ff4d87-d9a6-4533-836a-0c640034b8eb")

        try:

            ser = AddressSer(addres, many=True)
            alldata = ser.data

        except:
            alldata = ser.errors

        return Response(alldata)

    # orc PROFILE POST METHOD

    def post(self, request, pk=None):
        data = request.data
        usr = str(request.user.id)
        # usr = str("80d491f9-9671-48c0-8ab3-c7c4891687af")

        new_addres = {
            "fullname": data.get("fullname"),
            "phone": data.get("phone"),
            "email": data.get("email"),
            "house": data.get("house"),
            "trade": data.get("trade"),
            "area": data.get("area"),
            "city": data.get("city"),
            "pinCode": data.get("pinCode"),
            "delTime": data.get("delTime"),
            "state": data.get("state"),
            # "uplod": data.get("uplod"),
            "uplod": usr,
        }

        # print(new_addres)
        serializer = PostAddressSer(data=new_addres)

        # print(serializer)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            user = serializer.save()
            return Response(
                {
                    "stateCode": 200,
                    "msg": "enter data",
                }
            )
        return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)

    # orc Update Adress
    def put(self, request, pk=None):
        data = request.data
        idt = request.user.id
        # idt = request.data.get("id")

        cus = Address.objects.get(pk=idt)
        # print("this is profile id ,:- ", idt)

        # print(cus)
        # product_obj = Product.objects.get(id=product_id)
        new_address = {
            "fullname": data.get("fullname"),
            "phone": data.get("phone"),
            "email": data.get("email"),
            "house": data.get("house"),
            "trade": data.get("trade"),
            "area": data.get("area"),
            "city": data.get("city"),
            "pinCode": data.get("pinCode"),
            "delTime": data.get("delTime"),
            "state": data.get("state"),
            # "uplod": data.get("uplod"),
            # "uplod": usr,
        }

        # print(new_profile)
        serializer = PostProfileSer(cus, data=new_address)

        # print(serializer)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            user = serializer.save()
            return Response(
                {
                    "stateCode": 200,
                    "msg": "enter data",
                }
            )
        return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)
