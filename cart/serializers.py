from .models import Cart, CartItem
from rest_framework import serializers
from products.serializers import ProductSerializer
from accounts.models import User
from products.models import Product


class CartItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartItem
        fields = ['cart_item_id','product','quantity','unit']


class CartSerializer(serializers.ModelSerializer):
    items = CartItemSerializer(many = True)
   

    class Meta:
        model = Cart
        fields = ['cart_id',  'items']

    def create(self, validated_data):
        items_data = validated_data.pop('items')
        user = self.context.get('user')
        cart= Cart.objects.filter(customer = user).first()
        if cart is None:
            cart = Cart.objects.create(customer=user,**validated_data)
        else:
            cart = Cart.objects.filter(customer = user).first()
            cartitems = cart.items.all()
            cartitems.delete()

        for item_data in items_data:
            CartItem.objects.create(cart=cart, **item_data)

        return cart



# cart item views section
class CartItems_Serializer(serializers.ModelSerializer):
    product= ProductSerializer()
    class Meta:
        model = CartItem
        fields = ['cart_item_id','product','quantity']


class CartItemListSerializer(serializers.ModelSerializer):
    items = CartItems_Serializer(many = True, read_only = True)
    customer = serializers.SlugRelatedField(
        queryset=User.objects.all(), slug_field="name"
    )
    
    total_cost = serializers.SerializerMethodField()

    class Meta:
        model = Cart
        fields = ['cart_id', 'customer','total_cost', 'items']


    def get_total_cost(self, obj):
        return obj.get_total_cost()

    

