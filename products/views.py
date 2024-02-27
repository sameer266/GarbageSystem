from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import status
from rest_framework import generics
from . models import Category, SubCategory,Product,Banner,Advertisement
from .serializers import CategorySerializer, SubCategorySerializer,ProductSerializer,BannerSerializer,AdvertisementSerializer
from django.db.models import Q
from rest_framework import filters


''' Advertisement Banner '''
class AdvertisementListView(generics.ListAPIView):
    queryset = Advertisement.objects.all()
    serializer_class = AdvertisementSerializer

    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

''' bannar dssddggggggghhviews'''
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
        return super().list(request, *args, **kwargs)
    

''' sub category list with filter '''
class SubCategoryListView(generics.ListAPIView):
    serializer_class = SubCategorySerializer
    lookup_field = 'id'

    def get_queryset(self):
        id = self.kwargs.get('id')
        if id:
            queryset = SubCategory.objects.filter(
                Q(category__id=id) | Q(category__main_cateogry__id=id)
            ).distinct()  
        else:
            queryset = SubCategory.objects.all()

        return queryset
    
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)
    

'''product filter view'''
class CustomProductFilter(filters.BaseFilterBackend):
    def filter_queryset(self, request, queryset, view):
        product_name = request.query_params.get('product_name', None)
        category = request.query_params.get('category', None)
        sub_category = request.query_params.get('sub_category', None)
        rate = request.query_params.get('rate', None)

        filters_list = []

        if product_name:
            filters_list.append(Q(product_name__icontains=product_name))
        if rate:
            filters_list.append(Q(rate=rate))
        if category:
            filters_list.append(Q(category__category_name=category))
        if sub_category:
            filters_list.append(Q(sub_category__sub_catetegory_name=sub_category))

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
        return super().list(request, *args, **kwargs)