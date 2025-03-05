from django.shortcuts import get_object_or_404
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from .models import Cart,CartItem
from .serializers import CartSerializer,CartItemListSerializer,CartItemSerializer
from rest_framework.response import Response
from rest_framework import status
from rest_framework import generics,serializers

class CartItemViews(APIView):

    permission_classes=[IsAuthenticated]

    def get_queryset(self):
        user= self.request.user
        print(user)
        if user.is_user:
            return Cart.objects.filter(customer=user)
        if user.is_admin:
            return Cart.objects.all()


    def get(self, request, *args, **kwargs):
        queryset = self.get_queryset()  # Cart.objects.all()
        serializer = CartItemListSerializer(queryset, many=True)

        custom_response = {
            'data': serializer.data,
            'success': True,
            'status': status.HTTP_200_OK,
        }

        return Response(custom_response)
    
    def post(self, request):
        serializer = CartSerializer(data=request.data, context={'user': request.user})
        if serializer.is_valid():
            serializer.save()
            return Response({"msg": "Item added Successfully !", "data": serializer.data}, status=status.HTTP_200_OK)
        else:
            return Response({"data": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, *args, **kwargs):
        cart_id = kwargs.get('cart_id')
        user = request.user

        if not user.is_user:
            return Response({"message": "Permission Denied", "success": False}, status=status.HTTP_403_FORBIDDEN)

        cart_item = get_object_or_404(Cart, cart_id=cart_id)
        cart_item.delete()
        return Response({"message": "Cart Deleted Successfully!", "success": True}, status=status.HTTP_200_OK)




class CartItemUpdateRetrieveView(generics.RetrieveUpdateDestroyAPIView):
    queryset = CartItem.objects.all()
    serializer_class = CartItemSerializer
    lookup_field ='cart_item_id'
    permission_classes =[IsAuthenticated]

    def retrieve(self, request, *args, **kwargs):
        try:
            user = request.user
            if user.is_authenticated and user.is_user:
                return super().retrieve(request, *args, **kwargs)
        except serializers.ValidationError as e:
            error_messages = [str(error) for errors in e.detail.values() for error in errors]
            response = Response({'message': 'Validation Error', 'success': False, 'errors': error_messages}, status=status.HTTP_400_BAD_REQUEST)
            return response 

        response = Response({'message': 'Authentication Error', 'success': False}, status=status.HTTP_403_FORBIDDEN)
        return response
    

    def partial_update(self, request, *args, **kwargs):
        try:
            user = request.user
            if user.is_authenticated and user.is_user:
                response= super().partial_update(request, *args, **kwargs)
                response.data['message'] ="Updated Successfully !"
                response.data['success']= True
                response.status_code = status.HTTP_200_OK
                return response
        except serializers.ValidationError as e:
            error_messages = [str(error) for errors in e.detail.values() for error in errors]
            response = Response({'message': 'Validation Error', 'success': False, 'errors': error_messages}, status=status.HTTP_400_BAD_REQUEST)
            return response 

        response = Response({'message': 'Authentication Error', 'success': False}, status=status.HTTP_403_FORBIDDEN)
        return response
    
    def destroy(self, request, *args, **kwargs):
        try:
            user = request.user
            if user.is_authenticated and user.is_user:
                super().destroy(request, *args, **kwargs)
                return Response({"message":"Deleted Successfully !","success":True}, status= status.HTTP_200_OK)
        except serializers.ValidationError as e:
            error_messages = [str(error) for errors in e.detail.values() for error in errors]
            response = Response({'message': 'Validation Error', 'success': False, 'errors': error_messages}, status=status.HTTP_400_BAD_REQUEST)
            return response 

        response = Response({'message': 'Authentication Error', 'success': False}, status=status.HTTP_403_FORBIDDEN)
        return response