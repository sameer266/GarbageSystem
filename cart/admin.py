from django.contrib import admin
from .models import Cart, CartItem


class CartItemsAdmin(admin.TabularInline):
    model = CartItem

class CartAdmin(admin.ModelAdmin):
    inlines =[CartItemsAdmin]
    list_display = ['customer','cart_id']
admin.site.register(Cart,CartAdmin)
