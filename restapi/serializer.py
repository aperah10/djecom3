from rest_framework import serializers

# MY IMPORT FOR ALL FIELS
from accounts.models import *
from product.models import *
from customer.models import *

# ================

# make accounts in
class AccountsSeri(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ["email", "fullname", "phone", "password"]

        # fields = ('id', 'username', 'password',
        #           'first_name', 'last_name', 'email',)
        # extra_kwargs = {'password': {"write_only": True, 'required': True}}

        def create(self, validated_data):
            user = CustomUser.objects.create_user(**validated_data)
            # user = User.objects.create_user(validated_data['username'], validated_data['email'], validated_data['password'])
            # Token.objects.create(user=user)
            return user


# ---------------------------------------------------------------------------- #
#                    orc ProfilePage GET AND POST SERILIZER                    #
# ---------------------------------------------------------------------------- #

# PROFILE ACCOTUNS
class ProfileSer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = "__all__"


# ! PROFILE POST METHOD
class PostProfileSer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = [
            "fullname",
            "email",
            "pic",
            "gender",
        ]


# ---------------------------------------------------------------------------- #
#                       ! ADDRESS METHOD POST AND GET SERILIZER                                         #
# ---------------------------------------------------------------------------- #
class AddressSer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = "__all__"


class PostAddressSer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = [
            "fullname",
            "phone",
            "email",
            "house",
            "trade",
            "area",
            "city",
            "pinCode",
            "delTime",
            "state",
            "uplod",
        ]


# ALL PRODUCT SHOW DATA
class AllProductSer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = "__all__"
        depth = 1


# CART FOR DATA
class CartSer(serializers.ModelSerializer):
    class Meta:
        model = ProductInCart
        fields = "__all__"
        depth = 2


# ---------------------------------------------------------------------------- #
#                           orc CART ADDED SERILIZER                           #
# ---------------------------------------------------------------------------- #
class AddCartSer(serializers.ModelSerializer):
    class Meta:
        model = ProductInCart
        fields = ["product", "quantity", "customer_cart"]


# CART FOR DATA
class LikeSer(serializers.ModelSerializer):
    class Meta:
        model = Like
        fields = ["product", "user"]


# NOTIFICATION FOR DATA
class NotificationSer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = "__all__"
        # depth = 1


# ! ORDER PAGE METHOD
class AllOrderSer(serializers.ModelSerializer):
    class Meta:
        model = AllOrder
        fields = "__all__"
        # depth = 2


class CurrentOrderSer(serializers.ModelSerializer):
    class Meta:
        model = CurrentOrder
        fields = "__all__"
        # depth = 2
