from decimal import Decimal

from django.db import models
from django.utils.crypto import get_random_string
from django.core.validators import MinValueValidator,MaxValueValidator
from django.conf import settings


from shop.models import Product
from coupons.models import Coupon
from users.models import Address,PickupStation



class Order(models.Model):
    PENDING= 'pending'
    PROCESSING= 'processing'
    SHIPPED= 'shipped'
    OUT_FOR_DELIVERY = 'out_for_delivery'
    DELIVERED= 'delivered'
    CANCELLED= 'cancelled'

    STATUS_CHOICES = (
    ('pending','Pending'),
    ('processing','Processing'),
    ('shipped','Shipped'),
    ('out_for_delivery','Out for Delivery'),
    ('delivered','Delivered'),
    ('cancelled','Cancelled'),
    )
    user=models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, related_name='orders', 
        null=True, blank=True)
    address = models.ForeignKey(
        Address, on_delete=models.CASCADE, null=True, blank=True)
    pickup_station = models.ForeignKey(
        PickupStation, on_delete=models.CASCADE, null=True, blank=True)
    order_number = models.CharField(max_length=9, blank=True)
    coupon=models.ForeignKey(
        Coupon,related_name='orders',null=True,blank=True,on_delete=models.SET_NULL)
    discount= models.IntegerField(
        default=0,validators=[MinValueValidator(0),MaxValueValidator(100)])
    status=models.CharField(max_length=20,choices=STATUS_CHOICES,default='pending')
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    paid = models.BooleanField(default=False)

    class Meta:
        ordering = ['-created']
        indexes = [
            models.Index(fields=['-created']),
        ]

    def __str__(self):
        return f'Order {self.id}'
    

    def save(self, *args, **kwargs):
        if not self.order_number:
            self.order_number = get_random_string(
                length=9, allowed_chars='ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789')
        super().save(*args, **kwargs)


    def get_total_cost_before_discount(self):
        return sum(item.get_cost() for item in self.items.all())

    def get_discount(self):
        total_cost=self.get_total_cost_before_discount()
        if self.discount:
            return total_cost*(self.discount / Decimal(100))
        return Decimal(0)


    def get_total_cost(self):
        total_cost = self.get_total_cost_before_discount()
        return total_cost - self.get_discount()


class OrderItem(models.Model):
    order = models.ForeignKey(Order,
                              related_name='items',
                              on_delete=models.CASCADE)
    product = models.ForeignKey(Product,
                                related_name='order_items',
                                on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10,
                                decimal_places=2)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return str(self.id)

    def get_cost(self):
        return self.price * self.quantity