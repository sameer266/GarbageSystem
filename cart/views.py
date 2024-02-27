from django.shortcuts import get_object_or_404
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from .models import Cart,CartItem
from .serializers import CartSerializer,CartItemListSerializer
from rest_framework.response import Response
from rest_framework import status
from rest_framework import generics


class CartItemViews(generics.ListAPIView, generics.CreateAPIView):
    permission_classes=[IsAuthenticated]
    serializer_class = CartItemListSerializer
    def get_queryset(self):
        user= self.request.user
        if user :
            return Cart.objects.filter(customer=user)
            
        else:
            return Cart.objects.all()
            
    
    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset() 
        return super().list(request, *args, **kwargs)
    
    def post(self, request):
        print(request.user)
        serializer = CartSerializer(data=request.data, context={'user': request.user})
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Item added Successfully !", "data": serializer.data}, status=status.HTTP_200_OK)
        else:
            return Response({"message": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)







class CartItemsDeleteUpdate(generics.DestroyAPIView):
    lookup_field = 'id'
    serializer_class = CartSerializer
    permission_classes=[IsAuthenticated]
    def destroy(self, request, *args, **kwargs):
        try:
            cartID = Cart.objects.get(customer=request.user)
            cartID.delete()
            return Response({"message": "Cart Deleted Successfully!", "success": "true"}, status=status.HTTP_200_OK)

        except CartItem.DoesNotExist:
            return Response({"message": "Cart item not found!", "success": "false"}, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            return Response({"message": "Cart  not found !", "success": "false"}, status=status.HTTP_400_BAD_REQUEST)
    



