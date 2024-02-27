from django.urls import path
from . import views
from .views import CategoryListView, SubCategoryListView,ProductListView,BannerListView,AdvertisementListView

urlpatterns = [
    path('advertisement',AdvertisementListView.as_view(),name='advertisement'),
    path('banner',BannerListView.as_view(), name='bannar'),
    path('category', CategoryListView.as_view(), name='category'),
    path('category/<uuid:id>',SubCategoryListView.as_view(), name='sub_category_with_category'),
    path('sub-category', SubCategoryListView.as_view(), name='sub_category'),
    path('list',ProductListView.as_view(), name='product_list')
]
