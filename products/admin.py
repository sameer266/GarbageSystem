from django.contrib import admin
from . models import Category,Product,Unit,Banner,Vehicle,Advertisement,Invoice,Invoice_Item,Stock
from django.utils.html import format_html
from django.conf import settings

class AdvertisementAdmin(admin.ModelAdmin):
    model = Advertisement
    list_display =['id','display_banner']
    def has_add_permission(self, request):
        return not self.model.objects.exists()

    def has_delete_permission(self, request, obj=None):
        return self.model.objects.count() > 1
    def display_banner(self, obj):
        banner_url = obj.banner.url if obj.banner else settings.DEFAULT_UNKNOWN_PERSON_IMAGE_URL
        return format_html('<img src="{}" width="150" height="150" />', banner_url)

    display_banner.short_description = 'Advertisement Banner'
admin.site.register(Advertisement, AdvertisementAdmin)


class BannerAdmin(admin.ModelAdmin):
    model = Banner
    list_display =['title','image']
admin.site.register(Banner, BannerAdmin)

class CategoryAdmin(admin.ModelAdmin):
    model  = Category
    list_display =['id','image','ordering']
admin.site.register(Category,CategoryAdmin)


class UnitAdmin(admin.ModelAdmin):
    model = Unit
    list_display =['unit_name']
admin.site.register(Unit,UnitAdmin)

class ProductAdmin(admin.ModelAdmin):
    model = Product
    list_display = ['id','product_name','product_image','rate']
admin.site.register(Product,ProductAdmin)



class VehicleAdmin(admin.ModelAdmin):
    model = Vehicle
    list_display =['vehicle_number','driver']
admin.site.register(Vehicle,VehicleAdmin)


class StockAdmin(admin.ModelAdmin):
    model =Stock
    list_display =['id','product','quantity','sold_quantity']
admin.site.register(Stock,StockAdmin)


class InvoiceItemAdmin(admin.TabularInline):
    model  = Invoice_Item

class InvoceAdmin(admin.ModelAdmin):
    inlines =[InvoiceItemAdmin]
    list_display =['transaction','customer','total','date_created']
admin.site.register(Invoice,InvoceAdmin)