from decimal import Decimal
import uuid

from django.db import models
from django.utils.crypto import get_random_string
from django.utils.translation import gettext_lazy as _
from django.core.validators import MinValueValidator,MaxValueValidator
from django.conf import settings
from django.urls import reverse
from datetime import timedelta,timezone,datetime,date


from shop.models import Product,Coupon
from users.models import Address,PickupStation




class ShippingCompany(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100)
    description = models.TextField(blank=True)
    phone_number=models.CharField(max_length=15, blank=True, null=True)
    email=models.EmailField(blank=True, null=True)
    location=models.CharField(max_length=100,default='Nairobi')
    image = models.ImageField(upload_to='shipping_companies/', blank=True)
    uuid_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('name',)
        verbose_name = 'shipping company'
        verbose_name_plural = 'shipping companies'

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('orders:shipping_company_details', args=[self.slug])



class Order(models.Model):
    """Order model."""

    ORDER_STATUS =(
        ('pending', _('Pending')),
        ('waiting_fulfillment', _('Waiting Fulfillment')),
        ('processing', _('Processing')),
        ('shipped', _('Shipped')),
        ('out_for_delivery', _('Out for Delivery')),
        ('delivered', _('Delivered')),
        ('cancelled', _('Cancelled')),
    )

    PAYMENT_METHOD = (
        ('mpesa_on_deliverly', _('Mpesa on Delivery')),
        ('mpesa', _('Mpesa')),
        ('via_card', _('Via Card')),
        ('bank_transfer', _('Bank Transfer')),
        )

    
    user=models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, related_name='orders', 
        null=True, blank=True)
    address = models.ForeignKey(
        Address, on_delete=models.CASCADE, null=True, blank=True)
    pickup_station = models.ForeignKey(
        PickupStation, on_delete=models.CASCADE, null=True, blank=True)
    order_number = models.CharField(max_length=9, blank=True, null=True, unique=True)
    coupon=models.ForeignKey(Coupon, on_delete=models.SET_NULL, null=True, blank=True)
    order_status=models.CharField(
        max_length=50, choices=ORDER_STATUS, default='pending')
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    paid = models.BooleanField(default=False)
    payment_method = models.CharField(
        max_length=50, choices=PAYMENT_METHOD, default='mpesa_on_deliverly')
    returnable = models.BooleanField(default=True)
    delivered_by=models.ForeignKey(
        ShippingCompany,related_name='orders',null=True,blank=True,on_delete=models.SET_NULL)

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


    def get_absolute_url(self):
        return reverse('orders:order_detail', kwargs={'order_number': self.order_number})


    #method to apply coupon
    def apply_coupon(self,coupon):
        self.coupon=coupon
        self.save()


    def shipping_cost(self):
        shipping_cost=0
        for item in self.items.all():
            if item.product.size_of_package=='small':
                shipping_cost+=20
            elif item.product.size_of_package=='medium':
                shipping_cost+=50
            elif item.product.size_of_package=='large':
                shipping_cost+=70
            elif item.product.size_of_package=='extra large':
                shipping_cost+=100
            elif item.product.size_of_package=='extra extra large':
                shipping_cost+=150
        if self.address:
            if self.address.region=='Nairobi':
                shipping_cost+=100
            elif self.address.region=='Mombasa':
                shipping_cost+=200
            elif self.address.region=='Kisumu':
                shipping_cost+=300
            elif self.address.region=='Nakuru':
                shipping_cost+=400
            elif self.address.region=='Eldoret':
                shipping_cost+=500
            elif self.address.region=='Nyeri':
                shipping_cost+=600
            elif self.address.region=='Kakamega':
                shipping_cost+=700
            elif self.address.region=='Kisii':
                shipping_cost+=800
            elif self.address.region=='Meru':
                shipping_cost+=900
            elif self.address.region=='Nanyuki':
                shipping_cost+=1000
            elif self.address.region=='Kericho':
                shipping_cost+=1100
            elif self.address.region=='Kerugoya':
                shipping_cost+=1200
            elif self.address.region=='Kilifi':
                shipping_cost+=1300
            elif self.address.region=='Kisumu':
                shipping_cost+=1400
            elif self.address.region=='Kitale':
                shipping_cost+=1500
            elif self.address.region=='Kisumu':
                shipping_cost+=1600
            elif self.address.region=='Kisumu':
                shipping_cost+=1700
            elif self.address.region=='Kisumu':
                shipping_cost+=1800
            elif self.address.region=='Kisumu':
                shipping_cost+=1900
        return shipping_cost


    
    def get_total_cost(self):
        total_cost = sum(item.get_cost() for item in self.items.all())
        if self.coupon:
            total_cost=total_cost+self.shipping_cost()-self.coupon.value
        return total_cost
    
    def get_order_items(self):
        return self.items.all()

    '''
    a method to check if the order is returnable,
    if 15 days have elapsed from when the order status was set to delivered,
    flip the returnable field to false
    '''
    def check_returnable(self):
        if self.order_status=='delivered':
            if self.updated.date() + timedelta(days=15) < date.today():
                self.returnable=False
                self.save()
        return self.returnable

    #a method to show the returnable deadline date
    def get_returnable_deadline(self):
        if self.order_status=='delivered':
            return self.updated.date() + timedelta(days=15)
        return None

    #a method to check  deliverly method.if via pickup station or address
    #IF pickup station return via pickup station,if address return via Door Delivery
    def delivery_method(self):
        if self.pickup_station:
            return 'Pickup Station'
        elif self.pickup_station is None:
            return 'Door Delivery'
        return  'Door Delivery'


    #method to check shipping company,if None return Esoko Express Delivery
    def shipping_company(self):
        if self.delivered_by:
            return self.delivered_by.name
        return 'Esoko Express Delivery'
    
   
  
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