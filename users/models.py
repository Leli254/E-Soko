import uuid

from django.db import models
from django.utils.text import slugify
from django.utils.crypto import get_random_string
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _
from django.conf import settings
from django.urls import reverse

from .managers import UserManager


GENDER_CHOICES = (
    ('male', 'Male'),
    ('female','Female'),
    ('other', 'Other'))

REGIONS = (
        ('Nairobi',(
            ('Nairobi Central','Nairobi Central'),
            ('Nairobi CBD','Nairobi CBD'),
            ),
            ),
        ('Nakuru',(
            ('Nakuru Central','Nakuru Central'),
            ('Nakuru CBD','Nakuru CBD'),
            ),
        ),
    )
#a function to calclute shipping cost depending on the size of the order,and region


class User(AbstractUser):
    """User model."""

    username = None
    first_name=models.CharField(max_length=100, blank=True, null=True)
    last_name=models.CharField(max_length=100, blank=True, null=True)
    email = models.EmailField(_('email address'), unique=True)
    joindate=models.DateField(auto_now_add=True)
    uuid_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    phone_number = models.CharField(max_length=20)
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES,default='Male')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()
    
    
    class Meta:
        verbose_name = _("User")
        verbose_name_plural = _("Users")

    def __str__(self):
        return self.email

    
    
    @property
    def fullname(self):
        return f"{self.first_name} {self.last_name}"
    
    
    def has_address(self):
        return hasattr(self, 'address')
     
    


class Address(models.Model):
    """Address model."""
    user=models.ForeignKey(
        settings.AUTH_USER_MODEL,on_delete=models.CASCADE
        )
    address_name=models.CharField(max_length=100,verbose_name='Address Name',default='')
    region=models.CharField(max_length=200,choices=REGIONS,default='Nairobi')
    phone_number=models.CharField(max_length=20,verbose_name='Phone Number',default='')
    additional_phone_number=models.CharField(
        max_length=20,verbose_name='Additional Phone Number',blank=True,null=True)
    delivery_instructions=models.CharField(
        max_length=100,blank=True,null=True,
        verbose_name='Delivery Instructions |Additional Information')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    default_address=models.BooleanField(default=True)

    class Meta:
        verbose_name = _("Address")
        verbose_name_plural = _("Addresses")

    def __str__(self):
        return self.address_name

    
   #a method to prevent more than one default address
    def save(self, *args, **kwargs):
        if self.default_address:
            try:
                temp = Address.objects.get(default_address=True)
                if self != temp:
                    temp.default_address = False
                    temp.save()
            except Address.DoesNotExist:
                pass
        super(Address, self).save(*args, **kwargs)




class PickupStation(models.Model):
    name=models.CharField(max_length=100)
    address=models.CharField(max_length=100)
    phone_number=models.CharField(max_length=100)
    region=models.CharField(max_length=200,choices=REGIONS,default='Nairobi')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    default_station=models.BooleanField(default=False)


    class Meta: 
        verbose_name = _("Pickup Station")
        verbose_name_plural = _("Pickup Stations")
    
    

    def __str__(self):
        return self.name

    def  get_absolute_url(self):
        return reverse('pickupstation_detail', kwargs={'pk': self.pk})
    
    