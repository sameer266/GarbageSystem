from django.urls import path
from .views import *

urlpatterns = [
    path('', OrderListCreateView.as_view(), name='order-list-create'),
    path('order-items/create/', OrderItemCreateView.as_view(), name='order-item-create'),
    path('request-address/', RequestAddressCreateView.as_view(), name='request-address-create'),
    path('request-address/create/', RequestAddressCreateView.as_view(), name='request-address-create'),
    path('request-address/delete/<int:id>',RequestAddressDeleteView.as_view(), name='delete_address'),
    path('notifications',NotificationListView.as_view(), name='notification_list'),
    path('notifications/detail/<int:id>',NotificationRetrieveView.as_view(), name='notification_retrieve'),
]
