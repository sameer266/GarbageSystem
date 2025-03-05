from django.urls import path
from . import views
from .views import CategoryListView,ProductListView,BannerListView,AdvertisementListView,CategoryRelatedProductsListView

urlpatterns = [
    path('advertisement',AdvertisementListView.as_view(),name='advertisement'),
    path('banner',BannerListView.as_view(), name='bannar'),
    path('category', CategoryListView.as_view(), name='category'),
    path('list',ProductListView.as_view(), name='product_list'),
    path('category/product/<uuid:category_id>',CategoryRelatedProductsListView.as_view(), name='category_with_prodict'),
]
