from django.contrib import admin
from . models import Daily,DailyTransaction

class DailyTransactionAdmin(admin.TabularInline):
    model =  DailyTransaction

class DailyAdmin(admin.ModelAdmin):
    inlines =[DailyTransactionAdmin]
    list_display =['nepali_date','total']
admin.site.register(Daily,DailyAdmin)
