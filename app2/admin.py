from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import *


# Register your models here.
class AboutUSAdmin(admin.ModelAdmin):
    model = AboutUS
    list_display =['id','email','logo']
admin.site.register(AboutUS,AboutUSAdmin)


class PrivacyPolicyAdmin(admin.ModelAdmin):
    model = PrivacyPolicy
    list_display =['id','title']
admin.site.register(PrivacyPolicy,PrivacyPolicyAdmin)


admin.site.register(Customers)