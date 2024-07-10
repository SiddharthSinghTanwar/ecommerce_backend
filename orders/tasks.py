
from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings
from .models import Order

@shared_task
def send_order_confirmation_email(order_id):
    try:
        order = Order.objects.get(id=order_id)
        subject = f'Order Confirmation - Order #{order.id}'
        message = f'Thank you for your order. Your order #{order.id} has been received and is being processed.'
        from_email = settings.DEFAULT_FROM_EMAIL
        recipient_list = [order.user.email]
        send_mail(subject, message, from_email, recipient_list)
    except Order.DoesNotExist:
        print(f"Order with id {order_id} not found")