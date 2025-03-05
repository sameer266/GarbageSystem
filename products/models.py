import uuid
from django.db import models
from accounts.models import User
from autoslug import AutoSlugField
import random
from datetime import date
import nepali_datetime
from app2.models import Customers


class Banner(models.Model):
    title = models.CharField(max_length =150)
    image = models.ImageField(upload_to='bannarimage/')

    class Meta:
        ordering =['-id']

    def __str__(self):
        return self.title
    
class Advertisement(models.Model):
    banner = models.ImageField(upload_to='adertisementbabber/')

    class Meta:
        ordering=['-id']


class Category(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    category_name = models.CharField(max_length= 150)
    image = models.ImageField('categoryimage/')
    ordering = models.IntegerField(null =True, blank =True)

    class Meta:
        ordering =['ordering','id']

    def __str__(self):
        return self.category_name
 
'''product unit'''
class Unit(models.Model):
    unit_name = models.CharField(max_length=50)


    def __str__(self):
        return self.unit_name


'''products '''
class Product(models.Model):
    category = models.ForeignKey(Category, on_delete = models.CASCADE, related_name = 'product_category')
    product_name = models.CharField(max_length = 150)
    product_image = models.ImageField(upload_to='productimage/')
    previous_rate = models.FloatField(default=0)
    rate = models.FloatField()
    unit  = models.ForeignKey(Unit, on_delete= models.SET_NULL, null =True, blank=True, related_name ='product_unit')
    slug = AutoSlugField(populate_from ='product_name')
    order_number = models.IntegerField(null=True, blank=True, default=1)
    class Meta:
        ordering =['order_number']

    def __str__(self):
        return self.product_name
    

'''Vehicle’s '''
class Vehicle(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    vehicle_number = models.CharField(max_length = 50)
    driver = models.ForeignKey(User, on_delete = models.SET_NULL, null =True, blank=True)


    def __str__(self):
        return  self.driver.name + str(self.vehicle_number)
    

from django.utils import timezone
class Stock(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.FloatField(default=0)
    sold_quantity = models.FloatField(default=0)
    date_created = models.CharField(max_length=50,default=nepali_datetime.date.today().strftime("%d-%B-%Y"))
    date_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.product.slug + ' - ' + self.product.product_name



def generate_transaction_id():
    current_date = date.today().strftime('%Y%m%d')
    random_number = random.randint(1111, 9999)
    return str(current_date)+str(random_number)


class Invoice(models.Model):
    transaction = models.CharField(max_length = 250, default=generate_transaction_id, editable=False)
    customer = models.ForeignKey(Customers, on_delete=models.CASCADE,related_name='Customers',null=True,blank=True)
    total = models.FloatField(default= 0)
    date_created = models.CharField(max_length=50,default=nepali_datetime.date.today().strftime("%d-%B-%Y"), editable=False)

    def __str__(self):
        return self.transaction

    def item_count(self):
        return Invoice_Item.objects.filter(invoice = self).aggregate(Sum('quantity'))['quantity__sum']

    class Meta:
        ordering =['-id',]
    

class Invoice_Item(models.Model):
    invoice = models.ForeignKey(Invoice, on_delete=models.CASCADE, null=True, blank=True, related_name='invoice_items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    price = models.FloatField(default=0)
    quantity = models.FloatField(default=0)

    def get_cost(self):
        return self.quantity * self.price

    def update_stock(self):
        for item in Invoice.objects.get(invoice_items=self).invoice_items.all():
            try:
                stock = Stock.objects.get(product=item.product)
                stock.quantity -= item.quantity
                stock.sold_quantity += item.quantity
                stock.save()
            except Stock.DoesNotExist:
                pass

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.update_stock()
