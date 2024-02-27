from django.contrib import admin
from .models import Order, OrderItem,RequestAddress,Invoice,Pick_Up_Plan


admin.site.register(Pick_Up_Plan)


class RequestAddressAdmin(admin.ModelAdmin):
    model =RequestAddress
    list_display =['id','fullname','location','landmark','phoneNumber','alternativeNo']
admin.site.register(RequestAddress,RequestAddressAdmin)



class OrderItemInline(admin.TabularInline):
    model = OrderItem
   

class OrderAdmin(admin.ModelAdmin):
    inlines = [OrderItemInline]
    list_filter = ['payment_method', 'order_status']
    
admin.site.register(Order, OrderAdmin)




admin.site.register(Invoice)