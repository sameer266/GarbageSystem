from rest_framework import serializers
from . models import Category,Product,Unit,Banner,Advertisement


class AdvertisementSerializer(serializers.ModelSerializer):
    class Meta:
        model = Advertisement
        fields ='__all__'

class BannerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Banner
        fields = '__all__'

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'




class ProductUnitSerializer(serializers.ModelSerializer):
    class Meta:
        model  = Unit
        fields ='__all__'



class ProductSerializer(serializers.ModelSerializer):
    category = serializers.SlugRelatedField(
            queryset=Category.objects.all(), slug_field="category_name", required=False
        )
    
    unit = serializers.SlugRelatedField(
            queryset=Unit.objects.all(), slug_field="unit_name", required=False
        ) 
    class Meta:
        model  = Product 
        fields ='__all__'


