from django.db import models
import datetime
import nepali_datetime
from django.db.models.signals import pre_delete
from django.dispatch import receiver
from django.core.exceptions import ValidationError
from products.models import Product,Unit
from django.db.models.signals import post_save
from products.models import Stock
from django.utils import timezone


class Daily(models.Model):
    nepali_date =  models.CharField(max_length=50,default=nepali_datetime.date.today().strftime("%d-%B-%Y"))
    total = models.IntegerField(null=True, blank=True)

    class Meta:
        ordering =['-nepali_date',]

    def __str__(self):
        return str(self.nepali_date)
    

    def calculate_total_amount(self):
        total_amount = 0
        transactions = self.dailyId.all()  
        for transaction in transactions:
            total_amount += transaction.quantity * transaction.product.rate  
        self.total = total_amount
        self.save()
        return total_amount


    def get_grand_total(self):
        total = 0
        total += self.total
        return total
    
class DailyTransaction(models.Model):
    dailyid = models.ForeignKey(Daily, on_delete=models.CASCADE, related_name='dailyId', null=True, blank=True)
    product = models.ForeignKey(Product,on_delete=models.DO_NOTHING, db_constraint=False, related_name='daily_product')
    quantity = models.FloatField()
    unite = models.ForeignKey(Unit, on_delete=models.DO_NOTHING, db_constraint=False, related_name='daily_product_unit', null=True, blank=True)
    
    remarks = models.TextField()


    class Meta:
        ordering= ['-dailyid']

    def __str__(self):
        return str(self.product)
    

    def get_amount(self):
        amount = self.product.rate * self.quantity
        return amount


    def update_stock(self):
        try:
            stock, created = Stock.objects.get_or_create(product=self.product)
            stock.quantity += float(self.quantity)
            stock.save()
        except Stock.DoesNotExist:
            pass

    # def save(self, *args, **kwargs):
    #     super().save(*args, **kwargs)
    #     self.update_stock()


@receiver(post_save, sender=DailyTransaction)
def update_daily_total(sender, instance, **kwargs):
    instance.dailyid.calculate_total_amount()
  