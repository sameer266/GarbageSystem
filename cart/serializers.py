from .models import Cart, CartItem
from rest_framework import serializers
from products.serializers import ProductSerializer
from accounts.models import User
from products.models import Product
# from cart import Cart


class CartItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartItem
        fields = ['cart_item_id','cart','product','quantity', 'unit']




class CartSerializer(serializers.ModelSerializer):
    items = CartItemSerializer(many = True)
    # customer = serializers.SlugRelatedField(
    #     queryset=User.objects.all(), slug_field="name"
    # )

    class Meta:
        model = Cart
        fields = ['cart_id',  'items']

    def create(self, validated_data):
        items_data = validated_data.pop('items')
        user = self.context.get('user')
        cart= Cart.objects.filter(customer = user).first()
        if cart is None:
            print(cart)
            cart = Cart.objects.create(customer=user, **validated_data)
            for item_data in items_data:
                CartItem.objects.create(cart=cart, **item_data)
        else:
            for item_data in items_data:
                existing_item = cart.items.filter(product=item_data['product']).first()

                if existing_item:
                    existing_item.quantity += item_data.get('quantity', 1)
                    existing_item.save()
                else:
                    CartItem.objects.create(cart=cart, **item_data)


        return cart
    



# cart item views section
class CartItems_Serializer(serializers.ModelSerializer):
    product= ProductSerializer()
    class Meta:
        model = CartItem
        fields = ['cart_item_id','cart','product','quantity']


class CartItemListSerializer(serializers.ModelSerializer):
    items = CartItems_Serializer(many = True, read_only = True)
    customer = serializers.SlugRelatedField(
        queryset=User.objects.all(), slug_field="name"
    )
    class Meta:
        model = Cart
        fields = ['cart_id', 'customer', 'items']

    


