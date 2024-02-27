from django.urls import path
from . import views
from . views import CartItemViews,CartItemsDeleteUpdate


urlpatterns = [ 
    path('', CartItemViews.as_view()),
    path('delete/<int:id>',CartItemsDeleteUpdate.as_view(), name='cartitemdelete'),
]