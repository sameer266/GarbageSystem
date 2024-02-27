from django.urls import path
from . import views 
from django.contrib.auth import views as auth_views

from django.conf import settings
from django.conf.urls.static import static
from .views import *
from django.urls import re_path
from django.conf import settings
from django.views.static import serve
from django.conf.urls.static import static




app_name ='dashboard'
urlpatterns = [
        path('',views.index,name='index'),
        path('accounts/login/', login, name='login'),
        path('logout', views.userlogout, name='logout'),
    
        path('categorie',views.categories,name='Category'),
        path('categorie/add',views.add_edit_Category,name='add_Category'),
        path('categorie/edit/<uuid:id>/',views.add_edit_Category,name='edit_Category'),
        path('categorie/delete/<uuid:id>/',views.deleteCategory,name='deleteCategory'),


        path('product',views.Products,name='Product'),
        path('product/add',views.add_edit_Product,name='add_Product'),
        path('product/edit/<uuid:id>/',views.add_edit_Product,name='edit_Product'),
        path('product/delete/<uuid:id>/',views.deleteProduct,name='deleteProduct'),
        # path('get_subcategories/', get_subcategories, name='get_subcategories'),


        path('Vehicle',views.Vehicles,name='Vehicle'),
        path('Vehicle/add',views.add_edit_Vehicle,name='add_Vehicle'),
        path('Vehicle/edit/<uuid:id>/',views.add_edit_Vehicle,name='edit_Vehicle'),
        path('Vehicle/delete/<uuid:id>/',views.deleteVehicle,name='deleteVehicle'),
        
        path('Unit',views.Units,name='Unit'),
        path('Unit/add',views.add_edit_Unit,name='add_Unit'),
        path('Unit/edit/<int:id>/',views.add_edit_Unit,name='edit_Unit'),
        path('Unit/delete/<int:id>/',views.deleteUnit,name='deleteUnit'),
        
        path('Banner',views.Banners,name='Banner'),
        path('Banner/add',views.add_edit_Banner,name='add_Banner'),
        path('Banner/edit/<int:id>/',views.add_edit_Banner,name='edit_Banner'),
        path('Banner/delete/<int:id>/',views.deleteBanner,name='deleteBanner'),
        
        path('pick-up-Address',views.RequestAddresss,name='RequestAddress'),
        path('RequestAddress/delete/<int:id>/',views.deleteRequestAddress,name='deleteRequestAddress'),
        
        path('Advertisement',views.Advertisements,name='Advertisement'),
        path('Advertisement/add',views.add_edit_Advertisement,name='add_Advertisement'),
        path('Advertisement/edit/<int:id>/',views.add_edit_Advertisement,name='edit_Advertisement'),
        path('Advertisement/delete/<int:id>/',views.deleteAdvertisement,name='deleteAdvertisement'),
        
        path('SubCategory',views.SubCategories,name='SubCategory'),
        path('SubCategory/add',views.add_edit_SubCategory,name='add_SubCategory'),
        path('SubCategory/edit/<uuid:id>/',views.add_edit_SubCategory,name='edit_SubCategory'),
        path('SubCategory/delete/<uuid:id>/',views.deleteSubCategory,name='deleteSubCategory'),




        path('Order/add',views.create_Order,name='add_Order'),
        path('Order/edit/<int:id>/',views.create_Order,name='edit_Order'),

        path('active-order-list/', active_order_listListView.as_view(), name='active_order_list'),

        path('order-list-delete/<int:id>/', order_listDeleteView.as_view(), name='order_listdelete'),
        path('update-active-order-list/<int:id>/', views.update_active_order_list, name='update_active_order_list'),
        path('update-order-list/<int:id>/', views.update_order_list, name='update_order_list'),
        path('delivered-order-list-delete/<int:id>/', deliveredorder_listDeleteView.as_view(), name='deliveredorder_listdelete'),
        path('order-list/', order_listListView.as_view(), name='order_list'),

        path('add_driver/',DriverView.as_view(), name='add_Driver'),
        path('edit-driver/<int:id>/', DriverView.as_view(), name='edit_Driver'),
        path('driver/', DriverListView.as_view(), name='Driver'),
        path('driver-delete/<int:id>/', DriverDeleteView.as_view(), name='deleteDriver'),
        
        
        path('invoice-order/<int:id>/',  views.invoice1, name='invoice'),
        path('user/', UserListView.as_view(), name='User'),
        
        path('add-subadmin/',SubAdminView.as_view(), name='add_SubAdmin'),
        path('edit-SubAdmin/<int:id>/',SubAdminView.as_view(), name='edit_SubAdmin'),
        path('User-delete/<int:id>/', UserDeleteView.as_view(), name='deleteUser'),
        path('about-us', views.aboutUs, name='AboutUs'),
        
        path('order-details/<int:id>/', views.OrderDetail, name='OrderDetail'),
        
        path('add_Pick_Up_Plan/',views.add_edit_Pick_Up_Plan, name='add_Pick_Up_Plan'),
        path('edit_Pick_Up_Plan/<int:id>/', views.add_edit_Pick_Up_Plan, name='edit_Pick_Up_Plan'),
        path('delete_Pick_Up_Plan/<int:id>/', views.deletePick_Up_Plan, name='deletePick_Up_Plan'),

        path('change_password/', views.change_password, name='change_password'),

        # path('audio', views.audio, name='audio')

        # path('pcik-up/add', views.add_pick_up, name='add_pick_up'),

        path('accounting', views.accounting, name='accounting'),
        

        path('invoice/<int:order_id>', views.invoice, name='invoice'),
        path('invoice/edit', views.add_edit_invoice, name='edit_invoice'),

        path('cashbook/add',views.dailytransaction, name='daily_transaction'),
        path('cashbook',views.cashbook, name='cashbook'),
        path('cashbook/update/<int:id>',views.edite_dailytransaction, name='update_trasancation'),
        path('cashbook/delete',views.delete_transaction, name='delete_transaction'),
        path('cashbook/filter', views.dailytrasactionfilter, name='daily_tran_filter'),
        path('cashbook/item/delete', views.delete_daily_transaction_item, name='delete_items'),
        

        re_path(r"^media/(?P<path>.*)$", serve, {"document_root": settings.MEDIA_ROOT}),
        re_path(r"^static/(?P<path>.*)$", serve, {"document_root": settings.STATIC_ROOT}),

]+ static (settings.MEDIA_URL, document_root= settings.MEDIA_ROOT)