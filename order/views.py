from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status
from . models import Order,OrderItem,RequestAddress,Notification
from cart.models import Cart
from .serializers import OrderItemSerializer,OrderSerializer,RequestAddressSerializer,UserOrderSerializer,NotificationSerializers
from rest_framework.permissions import IsAuthenticated


''' order create and list views '''
class OrderListCreateView(generics.ListCreateAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes =[IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.is_user:
            queryset = Order.objects.filter(user= user)
            return queryset
        else:
            return None

    def get(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = UserOrderSerializer(queryset, many=True)
        return Response({"data":serializer.data, "success":True},status= status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        address_id = request.data.get('address')
        if address_id is not None:
            try:
                address = RequestAddress.objects.get(pk=address_id)
            except RequestAddress.DoesNotExist:
                return Response({"message": {"address": "Invalid address ID."}, "success": "false"}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"message": {"address": "Address ID is required."}, "success": "false"}, status=status.HTTP_400_BAD_REQUEST)

        serializer = OrderSerializer(data=request.data, context={'user': request.user, 'address': address})

        if serializer.is_valid():
            serializer.save(user=request.user, address=address)
            Cart.objects.filter(customer= request.user).delete()
            return Response({"message": "Order placed successfully!", "data": serializer.data, "success": "true"}, status=status.HTTP_201_CREATED)

        return Response({"message": serializer.errors, "success": "false"}, status=status.HTTP_400_BAD_REQUEST)


''' order item create '''
class OrderItemCreateView(generics.CreateAPIView):
    queryset = OrderItem.objects.all()
    serializer_class = OrderItemSerializer

    def perform_create(self, serializer):
        order_id = self.request.data.get('order')
        order = Order.objects.get(id=order_id)
        serializer.save(order=order)


''' add new address for order '''
class RequestAddressCreateView(generics.ListCreateAPIView):
    queryset = RequestAddress.objects.all()
    serializer_class = RequestAddressSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.is_user:
            queryset = RequestAddress.objects.filter(user= user)
            return queryset
        else:
            return None

    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data, context={'user': request.user})

        if serializer.is_valid():
            serializer.save(user=request.user) 
            return Response({"message": "New Address added successfully!", "data": serializer.data, "success": "true"}, status=status.HTTP_201_CREATED)
        return Response({"message": serializer.errors, "success": "false"}, status=status.HTTP_400_BAD_REQUEST)



''' address delete views'''
class RequestAddressDeleteView(generics.DestroyAPIView):
    queryset = RequestAddress.objects.all()
    serializer_class =  RequestAddressSerializer
    lookup_field ='id'

    def destroy(self, request, *args, **kwargs):
        super().destroy(request, *args, **kwargs)
        return Response({"message":"Address Deleted Successfully !", "success":True}, status=status.HTTP_200_OK)
    


'''notification '''
class NotificationListView(generics.ListAPIView):
    serializer_class = NotificationSerializers
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        queryset = Notification.objects.filter(user =user)
        return queryset
        
    def get(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response({"data": serializer.data, "success": True}, status=status.HTTP_200_OK)
    
    

class NotificationRetrieveView(generics.RetrieveAPIView):
    queryset = Notification.objects.all()
    serializer_class = NotificationSerializers
    permission_classes = [IsAuthenticated]
    lookup_field ='id'

    def get_object(self):
        obj = super().get_object()
        obj.read = True
        obj.save()
        return obj