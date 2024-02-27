from rest_framework import serializers
from products.models import Product,Unit
from accounts.models import User
from products.serializers import ProductSerializer
from .models import Order, OrderItem,RequestAddress
from cart.models import Cart
from accounts.models import User


'''user serializers '''
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'name', 'email','image']


''' address serializers '''
class RequestAddressSerializer(serializers.ModelSerializer):
    user = serializers.CharField(required=False)
    class Meta:
        model = RequestAddress
        fields = '__all__'


''' order item serializers '''
class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = ['product', 'quantity', 'unit']


'''order serializers '''
class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True)
    user = UserSerializer(read_only=True)
    address = RequestAddressSerializer(read_only=True)

    class Meta:
        model = Order
        fields = ['id', 'user', 'payment_method', 'order_status', 'totalPrice', 'created', 'updated', 'driver', 'items', 'address']

    def create(self, validated_data):
        items_data = validated_data.pop('items')
        address = validated_data.pop('address', None)

        if address:
            order = Order.objects.create(address=address, **validated_data)
        else:
            raise serializers.ValidationError({'address': 'Address is required'})

        for item_data in items_data:
            OrderItem.objects.create(order=order, **item_data)

        order.totalPrice = order.get_total_cost()
        order.save()

        return order



    