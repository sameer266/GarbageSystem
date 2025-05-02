from django.db import models
from django.core.validators import RegexValidator
from accounts.models import User, UserReward, Reward
from products.models import Product, Unit, Stock
import nepali_datetime
from django.utils import timezone
from accounting.models import Daily, DailyTransaction
from django.dispatch import receiver
from django.db.models.signals import post_save, pre_save

# Phone number validator
phone_validator = RegexValidator(
    r'\d{3}?-?\d{3}?-?\d{4}', 'Only ten numbers and dashes allowed.'
)

class RequestAddress(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='request_address')
    fullname = models.CharField(max_length=150)
    location = models.CharField(max_length=150)
    landmark = models.CharField(max_length=150, null=True, blank=True)
    phoneNumber = models.CharField(max_length=150, validators=[phone_validator])
    alternativeNo = models.CharField(max_length=150, null=True, blank=True)

    def __str__(self):
        return f"Request Address for {self.user.name}"


class Notification(models.Model):
    TYPE=(
        ('order', 'Order'),
        ('system', 'System'),
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    type = models.CharField(max_length=50, choices=TYPE, default='order')
    image=models.ImageField(upload_to='system_notification_image/',null=True,blank=True)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    read = models.BooleanField(default=False)
    order_number = models.PositiveIntegerField(null=True,blank=True)

    class Meta:
        ordering = ['-id']

    def __str__(self):
        return f"Notifications of {self.user.name} - {self.message}"


from django.db.models.signals import post_delete
from django.dispatch import receiver
import os


@receiver(post_delete, sender=Notification)
def delete_notification_image(sender, instance, **kwargs):
    if instance.image:
        if os.path.isfile(instance.image.path):
            os.remove(instance.image.path)
            
            
from django.db import models
from django.utils.timezone import now
from django.db.models.signals import pre_save
from django.dispatch import receiver
import math

class Order(models.Model):
    PAYMENT_CHOICES = [('cod', 'Cash on Delivery')]
    ORDER_STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('accept', 'Accepted'),
        ('rdp', 'Ready To Pick Up'),
        ('received', 'Received')
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, limit_choices_to={'is_user': True}, related_name='orders')
    payment_method = models.CharField(max_length=50, choices=PAYMENT_CHOICES, default='cod')
    order_status = models.CharField(max_length=50, choices=ORDER_STATUS_CHOICES, default="pending")
    totalPrice = models.FloatField(null=True, blank=True)
    created = models.CharField(max_length=50, default=nepali_datetime.date.today().strftime("%d-%B-%Y"), editable=False)
    updated = models.DateTimeField(auto_now=True)
    driver = models.ForeignKey(User, on_delete=models.SET_NULL, limit_choices_to={'is_agent': True}, null=True, blank=True)
    address = models.ForeignKey(RequestAddress, on_delete=models.SET_NULL, null=True, blank=True, related_name='order_address')
    order_status_changed = models.DateTimeField(null=True, blank=True)  # Track order status change time

    def __str__(self):
        return f"Order {self.id} - {self.user}"

    def get_total_cost(self):
        cost=sum([item.get_cost() for item in self.items.all()])
        return int(math.ceil(cost/5.0))*5

    def update_stock(self):
        if self.order_status == 'received':
            for item in self.items.all():
                stock, created = Stock.objects.get_or_create(
                    product=item.product,
                    defaults={'quantity': item.quantity, 'date_created': now()}
                )
                if not created:
                    stock.quantity += item.quantity
                    stock.save()

                daily, _ = Daily.objects.get_or_create(nepali_date=nepali_datetime.date.today().strftime("%d-%B-%Y"))
                DailyTransaction.objects.create(
                    dailyid=daily,
                    product=item.product,
                    quantity=item.quantity,
                    unite=item.product.unit,
                    remarks=f"Received from Order {self.id}"
                )

            if self.totalPrice:
                reward = Reward.objects.first()
                if reward:
                    user_reward, created = UserReward.objects.get_or_create(
                        user=self.user,
                        defaults={'points': round(self.totalPrice * reward.percentage / 100, 2), 'total_transaction_amount': self.totalPrice}
                    )
                    if not created:
                        user_reward.points += round(self.totalPrice * reward.percentage / 100, 2)
                        user_reward.total_transaction_amount += self.totalPrice
                        user_reward.save()

    def save(self, *args, **kwargs):
        if hasattr(self, '_disable_save'):
            return  # Prevent recursion
        self._disable_save = True  # Set flag to prevent recursion

        is_new = self.pk is None
        super().save(*args, **kwargs)

        if not is_new and self.order_status == 'received':
            self.update_stock()

        del self._disable_save  # Remove flag after saving


@receiver(pre_save, sender=Order)
def pre_save_order(sender, instance, **kwargs):
    if instance.id:  # Ensure the order exists
        try:
            previous_order = Order.objects.get(id=instance.id)
            if instance.order_status != previous_order.order_status:
                instance.order_status_changed = now()  # Set timestamp if status changed
        except Order.DoesNotExist:
            instance.order_status_changed = now()  # Set timestamp for new orders
    else:
        instance.order_status_changed = now()  # New orders always have a timestamp


@receiver(post_save, sender=Order)
def create_order_notification(sender, instance, created, **kwargs):
    if created:
        message = f"Order placed successfully! Your Order Number is {instance.id}."
        Notification.objects.create(user=instance.user, message=message, order_number=instance.id)
    elif instance.order_status_changed:
        message = f"Order status for Order Number #{instance.id} has been changed to {instance.order_status}."
        Notification.objects.create(user=instance.user, message=message, order_number=instance.id)
        instance.order_status_changed = False  # Reset the flag
        instance.save()  # Save the instance to update the flag


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items', null=True, blank=True)
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True, blank=True, related_name="order_product")
    quantity = models.PositiveIntegerField(default=1)
    unit = models.ForeignKey(Unit, on_delete=models.SET_NULL, null=True, blank=True)
    ordered_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.id}"

    def get_cost(self):
        return self.product.rate * self.quantity

    class Meta:
        ordering = ('-ordered_date',)


class Pick_Up_Plan(models.Model):
    address = models.CharField(max_length=50)
    message = models.TextField()
    date = models.CharField(max_length=50, default=nepali_datetime.date.today().strftime("%d-%B-%Y"))
    driver = models.ForeignKey(User, on_delete=models.CASCADE, limit_choices_to={'is_agent': True}, related_name='pick_up_plan_driver')

    def __str__(self):
        return f"{self.address}: {self.message}"