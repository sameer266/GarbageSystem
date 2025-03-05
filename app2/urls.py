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
        path('privacy-policy/', views.privacy, name='privacy'),
        
        
        path('customer-invoice/<int:customer_id>/', views.customer_invoices, name='customer_invoices'),

    
        path('categorie',views.categories,name='Category'),
        path('categorie/add',views.add_edit_Category,name='add_Category'),
        path('categorie/edit/<uuid:id>/',views.add_edit_Category,name='edit_Category'),
        path('categorie/delete/<uuid:id>/',views.deleteCategory,name='deleteCategory'),


        path('product',views.Products,name='Product'),
        path('product/add',views.add_edit_Product,name='add_Product'),
        path('product/edit/<int:id>/',views.add_edit_Product,name='edit_Product'),
        path('product/delete/<int:id>/',views.deleteProduct,name='deleteProduct'),
        # path('get_subcategories/', get_subcategories, name='get_subcategories'),

        path('suppliers',views.Customerss,name='Customers'),
        path('suppliers/add',views.add_edit_Customers,name='add_Customers'),
        path('suppliers/edit/<int:id>/',views.add_edit_Customers,name='edit_Customers'),
        path('suppliers/delete/<int:id>/',views.deleteCustomers,name='deleteCustomers'),
        path('suppliers/export/<format>',views.export_data, name='export_data'),

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
        
        

        path('Order/add',views.create_Order,name='add_Order'),
        path('Order/edit/<int:id>/',views.create_Order,name='edit_Order'),
        # path('Order/calculate-price/',views.CalculatePrice.as_view(),name='calculate_price'),

        path('active-order-list/', active_order_listListView.as_view(), name='active_order_list'),

        path('order-list-delete/<int:id>/', order_listDeleteView.as_view(), name='order_listdelete'),
        path('update-active-order-list/<int:id>/', views.update_active_order_list, name='update_active_order_list'),
        path('update-order-list/<int:id>/', views.update_order_list, name='update_order_list'),
        path('delivered-order-list-delete/<int:id>/', deliveredorder_listDeleteView.as_view(), name='deliveredorder_listdelete'),
        path('order-list/', order_listListView.as_view(), name='order_list'),

        path('add_driver/',DriverView.as_view(), name='add_Driver'),
        path('driver/', DriverListView.as_view(), name='Driver'),
        path('driver-delete/<int:id>/', DriverDeleteView.as_view(), name='deleteDriver'),
        path('edit-driver/<int:id>/', UpdateAgentView.as_view(), name='update_agent'),

        
        path('edit_profile',views.edit_profile,name="edit_profile"),

        path('invoice-order/<int:id>/',  views.invoice1, name='invoice'),
        path('user/', UserListView.as_view(), name='User'),
        
        path('add-subadmin/',SubAdminView.as_view(), name='add_SubAdmin'),
        path('sub-admin-delete/<int:id>/', SubAdminDeleteView.as_view(), name='deleteSubAdmin'),
        path('sub-admin/', SubAdminListView.as_view(), name='SubAdmin'),
        path('edit-SubAdmin/<int:id>/',UpdateSubAdminView.as_view(), name='edit_Sub_Admin'),


        path('User-add',views.UserAdd.as_view(),name="add_user"),
        path('User-delete/<int:id>/', UserDeleteView.as_view(), name='deleteUser'),
        path('about-us', views.aboutUs, name='AboutUs'),
        
        path('order-details/<int:id>/', views.OrderDetail, name='OrderDetail'),
        path('pick_up_plan', views.pick_Up_plans, name='pick_up_plans'),
        path('add_pick_up_plan/',views.add_edit_Pick_Up_Plan, name='add_Pick_Up_Plan'),
        path('edit_pick_up_plan/<int:id>/', views.add_edit_Pick_Up_Plan, name='edit_Pick_Up_Plan'),
        path('delete_pick_up_plan/<int:id>/', views.deletePick_Up_Plan, name='deletePick_Up_Plan'),

        path('change_password/', views.change_password, name='change_password'),

        # path('audio', views.audio, name='audio')

        # path('pcik-up/add', views.add_pick_up, name='add_pick_up'),

        path('accounting', views.accounting, name='accounting'),
        

        path('invoice/<int:order_id>', views.invoice, name='invoice'),
        path('invoice/edit', views.add_edit_invoice, name='edit_invoice'),

        path('cashbook/add',views.dailytransaction, name='daily_transaction'),
        # path('cashbook',views.cashbook, name='cashbook'),
        path('cashbook/update/<int:id>',views.edite_dailytransaction, name='update_trasancation'),
        path('cashbook/delete',views.delete_transaction, name='delete_transaction'),
        path('cashbook/filter', views.dailytrasactionfilter, name='daily_tran_filter'),
        path('cashbook/item/delete', views.delete_daily_transaction_item, name='delete_items'),
        
        path('inventory',views.inventory, name="inventory"),
        path('inventory-add',views.inventory_add,name="inventory_add"),
        path('inventory-edit/<int:id>/', views.edit_inventory, name='edit_inventory'),
        path('sales', views.sales, name='sales'),
        path('sales/create', views.create_sales, name='create_sales'),
        path('sales/detail/<int:id>', views.sales_details, name='sales_details'),
        path('sales/invoice/<int:id>', views.sales_invoice, name='sale_invoice'),
        
        path('save_sales',views.save_sales, name="save-sales"),
        path('get_product',views.get_product,name='get-product'),
        path('get_product',views.get_product, name='get_product_data'),
        
        path('rewards', views.rewards_create_or_update, name='rewards_create_or_update'),
        path('order/history/<int:id>',views.user_order_history, name='user_order_history'),
        path('reward/update/<int:id>',views.user_reward_update, name='user_reward_update'),
        
        # ==== notofication =======
        path('notification_list',views.notification_list,name="notification_list"),
        


        re_path(r"^media/(?P<path>.*)$", serve, {"document_root": settings.MEDIA_ROOT}),
        re_path(r"^static/(?P<path>.*)$", serve, {"document_root": settings.STATIC_ROOT}),

]+ static (settings.MEDIA_URL, document_root= settings.MEDIA_ROOT)