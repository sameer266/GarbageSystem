from accounts.models  import User
from order.models import Order,Pick_Up_Plan
from django.db.models import Sum
from django.db.models import Q
from datetime import datetime
from accounting.models import Daily
import nepali_datetime
from dateutil.relativedelta import relativedelta
from datetime import date,timedelta

from app2.models import AboutUS


def aboutus(request):
    pick_Up_Plans=Pick_Up_Plan.objects.all()
    aboutus = AboutUS.objects.first()
    return {'contact': aboutus,'details':pick_Up_Plans,'company':aboutus}




def usercount(request):
    totalClient = User.objects.filter(is_user= True).count
    return ({
        'totalClient':totalClient
    })


def invoice(request):
    received_orders = Order.objects.filter(order_status='received')
    paid_amount = received_orders.aggregate(total_cost=Sum('totalPrice'))['total_cost'] or 0
    order = Order.objects.all().count

    unreceived_orders = Order.objects.exclude(Q(order_status='received') | Q(order_status='pending'))
    unpaid_amount = unreceived_orders.aggregate(total_cost=Sum('totalPrice'))['total_cost'] or 0


    return({
        'paidamount':paid_amount,
        'totalOrders':order,
        'unpaidamount':unpaid_amount
    })

def notification(request):
    notifications = Pick_Up_Plan.objects.filter(date=datetime.today())
    return({
        'notifications':notifications
    })


def total_cashbook(request):
    dailytransactions_list = Daily.objects.all()
    grand_total = dailytransactions_list.aggregate(Sum('total'))['total__sum']

   
    return ({
        'grand_total':grand_total,
       
    })