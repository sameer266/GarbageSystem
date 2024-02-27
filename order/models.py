from django.db import models
from django.core.validators import RegexValidator
from accounts.models import User
from products.models import Product,Unit
import datetime

phone_validator = RegexValidator(
    r'\d{3}?-?\d{3}?-?\d{4}', 'Only ten numbers and dashes allowed.')

class RequestAddress(models.Model):
    user = models.ForeignKey(User,on_delete = models.CASCADE, related_name = 'request_address')
    fullname = models.CharField(max_length=150)
    location= models.CharField(max_length=150)
    landmark= models.CharField(max_length=150,null=True, blank=True)
    phoneNumber = models.CharField(max_length=150)
    alternativeNo= models.CharField(max_length=150, null=True, blank=True,)


    def __str__(self):
        return f"Request Address for {self.user.name}"
    
class Order(models.Model):
    PAYMENT_CHOICES = [('cod', 'Cash on Delivery')]

    ORDER_STATUS_CHOICES = [('pending', 'Pending'),
                            ('accept','Accepted'),
                            ('rdp', 'Ready To Pick Up'), 
                            ('received', 'Received')
                            ]

    user = models.ForeignKey(User, on_delete = models.CASCADE, related_name = 'orders')
    payment_method = models.CharField(max_length = 50, choices = PAYMENT_CHOICES, default= 'cod')
    order_status = models.CharField(max_length = 50, choices = ORDER_STATUS_CHOICES, default="pending")
    totalPrice = models.FloatField(null=True, blank=True)
    created = models.DateTimeField(auto_now_add = True)
    updated = models.DateTimeField(auto_now = True)
    driver = models.OneToOneField(User, on_delete=models.CASCADE,limit_choices_to={'is_agent': True}, null=True, blank=True)
    address = models.OneToOneField(RequestAddress, on_delete=models.SET_NULL, null=True, blank=True, related_name ='order_address')

    def __str__(self):
        return f"Order {self.id} - {self.user}"
    
    def get_total_cost(self):
        return sum([item.get_cost() for item in self.items.all()])

    

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete = models.CASCADE, related_name = 'items',  null=True, blank=True)
    product = models.ForeignKey(Product, on_delete = models.SET_NULL,  null= True, blank =True,related_name="order_product")
    quantity = models.PositiveIntegerField(default = 1)
    unit = models.ForeignKey(Unit, on_delete= models.SET_NULL, null=True, blank =True)
    ordered_date = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.id}"
    
    def get_cost(self):
        return self.product.rate * self.quantity
    
    class Meta:
        ordering = ('-ordered_date',)

import random 


import datetime
from django.db import models

def generate_invoice_number():
    last_invoice = Invoice.objects.order_by('-invoice_number').first()
    if last_invoice:
        last_number = int(last_invoice.invoice_number)
        new_invoice_number = str(last_number + 1).zfill(4)
    else:
        new_invoice_number = '0001'
    return new_invoice_number

Invoice_status =(
    ('paid','Paid'),
    ('unpaid','Unpaid')
)

class Invoice(models.Model):
    user = models.ForeignKey(User, on_delete= models.SET_NULL, null=True, blank=True)
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='order_invoice')
    invoice_date = models.DateField(default=datetime.date.today)
    invoice_number = models.CharField(max_length=4, unique=True, default=generate_invoice_number, editable=True)
    summery= models.CharField(max_length= 200)
    note = models.TextField()
    invoice_statu =models.CharField(max_length=50,choices =Invoice_status, default= 'unpaid')

    def __str__(self):
        return str(self.invoice_number) + str(self.order) +str(self.invoice_date)

import nepali_datetime
class Pick_Up_Plan(models.Model):
    address = models.CharField(max_length =50)
    message = models.TextField()
    date = models.CharField(max_length=50,default=nepali_datetime.date.today().strftime("%d-%B-%Y"))
    driver = models.ForeignKey(User, on_delete=models.CASCADE,limit_choices_to={'is_agent': True}, related_name='pick_up_plan_driver')

    def __str__(self):
        return f"{self.address}: {self.message}"
