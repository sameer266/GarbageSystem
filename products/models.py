import uuid
from django.db import models
from accounts.models import User


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
    

class SubCategory(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    category = models.ForeignKey(Category, on_delete= models.SET_NULL, null=True, blank=True, related_name = 'main_cateogry')
    sub_category_name  = models.CharField(max_length= 150)
    image = models.ImageField(upload_to='subcategoryimage/')
    ordering = models.IntegerField(null=True, blank=True)


    class Meta:
        ordering =['ordering','id']

    def __str__(self):
        return self.sub_category_name


'''product unit'''
class Unit(models.Model):
    unit_name = models.CharField(max_length=50)


    def __str__(self):
        return self.unit_name


'''products '''
class Product(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    category = models.ForeignKey(Category, on_delete = models.CASCADE, related_name = 'product_category')
    sub_category = models.ForeignKey(SubCategory, on_delete= models.CASCADE, related_name = 'product_sub_category')
    product_name = models.CharField(max_length = 150)
    product_image = models.ImageField(upload_to='productimage/')
    rate = models.FloatField()
    unit  = models.ForeignKey(Unit, on_delete= models.SET_NULL, null =True, blank=True, related_name ='product_unit')
    class Meta:
        ordering =['-id']

    def __str__(self):
        return self.product_name
    

'''Vehicle’s '''
class Vehicle(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    vehicle_number = models.CharField(max_length = 50)
    driver = models.ForeignKey(User, on_delete = models.SET_NULL, null =True, blank=True)


    def __str__(self):
        return  self.driver.name + str(self.vehicle_number)