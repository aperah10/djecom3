from rest_framework import serializers 

# MY IMPORT FOR ALL FIELS  
from accounts.models import * 
from product.models import * 
# ================

# make accounts in 
class AccountsSeri(serializers.ModelSerializer):

    class Meta:
        model =CustomUser 
        fields=['email','fullname','phone','password'] 

        # fields = ('id', 'username', 'password',
        #           'first_name', 'last_name', 'email',)
        # extra_kwargs = {'password': {"write_only": True, 'required': True}}

        def create(self, validated_data):
            user = CustomUser.objects.create_user(**validated_data)
            # user = User.objects.create_user(validated_data['username'], validated_data['email'], validated_data['password'])
            # Token.objects.create(user=user)
            return user



# PROFILE ACCOTUNS 
class ProfileSeri(serializers.ModelSerializer):

    class Meta:
        model=Profile 
        fields='__all__'


# ALL PRODUCT SHOW DATA 
class AllProductSer(serializers.ModelSerializer):

    class Meta: 
        model=Product
        fields='__all__' 
        depth = 1

# CART FOR DATA 
class CartSer(serializers.ModelSerializer):

    class Meta: 
        model=ProductInCart 
        fields ='__all__'
        


# CART FOR DATA 
class LikeSer(serializers.ModelSerializer):

    class Meta: 
        model=Like
        fields =['product','user']


# NOTIFICATION FOR DATA 
class NotificationSer(serializers.ModelSerializer):

    class Meta: 
        model=Notification
        fields ='__all__' 
        # depth = 1

