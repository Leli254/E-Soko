from celery import shared_task
from django.core.mail import send_mail
from .models import Order


@shared_task
def order_created(order_id):
    """
    Task to send an e-mail notification when an order is
    successfully created.
    """
    order = Order.objects.get(id=order_id)
    subject = f'Order nr. {order.order_number  }'
    message = f'Dear {order.first_name},\n\n' \
              f'You have successfully placed an order.' \
              f'Your order Number is {order.order_number}.'
    mail_sent = send_mail(subject,
                          message,
                          'admin@myshop.com',
                          [order.email])
    return mail_sent

@shared_task
def order_confirmed(order_id):
    """
    Task to send an e-mail notification when an order is
    successfully confirmed.
    """
    order = Order.objects.get(id=order_id)
    subject = f'Order nr. {order.order_number}'
    message = f'Dear {order.first_name},\n\n' \
              f'Your order has been confirmed.' \
              f'Your order ID is {order.order_number}.'
    mail_sent = send_mail(subject,message,'admin@esoko.com',[order.email]) 
    return mail_sent