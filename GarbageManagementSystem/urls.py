"""
URL configuration for GarbageManagementSystem project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/account/',include('accounts.urls')),
    path('api/product/',include('products.urls')),
    path('api/cart/',include('cart.urls')),
    path('api/orders/',include('order.urls')),
    path('',include('app2.urls')),
    
]+ static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)


handler404 = "app2.views.custom_404_view"