from celery import shared_task
from .models import Subscription
from datetime import  date
# saas/tasks.py
from celery import shared_task
import logging


@shared_task
def update_recurring_subscriptions():
    subscriptions = Subscription.objects.filter(is_recurring=True)
    for subscription in subscriptions:
        if subscription.payment_date <= date.today():
            subscription.update_payment_date()

            
@shared_task
def add_numbers(x, y, r):
    result = x + y + r
    print(f"Task completed! The result of {x} + {y} is {result}.")
    return result


# Set up logger for debugging
logger = logging.getLogger(__name__)

@shared_task
def print_hello():
    logger.info("Hello, the task is running! HELLO THIS I RUNNIGN ")
    print("Hello, the task is running!")
