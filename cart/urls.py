from django.urls import path, include
from rest_framework.routers import SimpleRouter
from . import views
from . views import CartItemViews,CartItemUpdateRetrieveView


urlpatterns = [ 
    path('', CartItemViews.as_view()),
    path('delete/<uuid:cart_id>', CartItemViews.as_view(),name='cart_delete'),
    path('item/detail/<uuid:cart_item_id>',CartItemUpdateRetrieveView.as_view(), name='cart_detail'),
    path('item/update/<uuid:cart_item_id>',CartItemUpdateRetrieveView.as_view(), name='cart_update'),
    path('item/delete/<uuid:cart_item_id>',CartItemUpdateRetrieveView.as_view(), name='cart_delete')
]