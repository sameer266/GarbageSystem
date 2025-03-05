from django.shortcuts import render,get_object_or_404
from rest_framework.response import Response
from rest_framework import status
from rest_framework import generics
from . models import Category,Product,Banner,Advertisement
from .serializers import CategorySerializer,ProductSerializer,BannerSerializer,AdvertisementSerializer
from django.db.models import Q
from rest_framework import filters


''' Advertisement Banner '''
class AdvertisementListView(generics.ListAPIView):
    queryset = Advertisement.objects.all()
    serializer_class = AdvertisementSerializer

    def list(self, request, *args, **kwargs):
        response = super().list(request, *args, **kwargs)
        return Response({'data':response.data, 'success':True}, status=status.HTTP_200_OK)

''' bannar views'''
class BannerListView(generics.ListAPIView):
    queryset = Banner.objects.all()
    serializer_class = BannerSerializer

    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)
        
''' Category views '''
class CategoryListView(generics.ListAPIView):
    queryset  = Category.objects.all()
    serializer_class =  CategorySerializer

    def list(self, request, *args, **kwargs):
        response = super().list(request, *args, **kwargs)
        return Response({'data':response.data,'success':True}, status=status.HTTP_200_OK)
    

'''product filter view'''
class CustomProductFilter(filters.BaseFilterBackend):
    def filter_queryset(self, request, queryset, view):
        product_name = request.query_params.get('product_name', None)
        category = request.query_params.get('category', None)
        rate = request.query_params.get('rate', None)

        filters_list = []

        if product_name:
            filters_list.append(Q(product_name__icontains=product_name))
        if rate:
            filters_list.append(Q(rate=rate))
        if category:
            filters_list.append(Q(category__category_name=category))
       
        if filters_list:
            queryset = queryset.filter(*filters_list)

        return queryset



''' product list'''

class ProductListView(generics.ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    search_fields = ['product_name', 'rate']
    filter_backends = (CustomProductFilter,filters.SearchFilter,)

    def list(self, request, *args, **kwargs):
        response= super().list(request, *args, **kwargs)
        return Response({'data':response.data,'success':True}, status=status.HTTP_200_OK)

''' category related products'''
class CategoryRelatedProductsListView(generics.ListAPIView):
    serializer_class = ProductSerializer

    def get_queryset(self):
        category_id = self.kwargs['category_id']
        category = get_object_or_404(Category, id=category_id)
        return Product.objects.filter(category=category).order_by('-id')
    
    def get(self, request, *args, **kwargs):
        response = super().get(request, *args, **kwargs)
        return Response({'data':response.data,'success':True}, status=status.HTTP_200_OK)