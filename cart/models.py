from django.db import models
from products.models import Product,Unit
from accounts.models import User
import uuid


class Cart(models.Model):
    cart_id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )

    customer = models.ForeignKey(User, on_delete=models.CASCADE,limit_choices_to={'is_user': True}, related_name = 'cart')

    def get_total_cost(self):
        return sum([item.get_cost() for item in self.items.all()])
    
    def __str__(self):
        return "cart items" + " "+ str(self.customer)+" "+ str(self.cart_id)

class CartItem(models.Model):
    cart_item_id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )
    cart = models.ForeignKey(Cart, on_delete = models.CASCADE, related_name = 'items', null=True, blank=True)
    product = models.ForeignKey(Product, on_delete = models.CASCADE, related_name ='cart_product')
    quantity = models.PositiveIntegerField(null=True, blank=True)
    unit  = models.ForeignKey(Unit, on_delete = models.CASCADE, related_name ='cart_product_unit')
    
    def get_cost(self):
        return self.product.rate * self.quantity
    
    def __str__(self):
        return str(self.cart)
    



