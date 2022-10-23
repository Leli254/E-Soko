import uuid
from django.db import models
from django.utils.text import slugify
from django.utils.crypto import get_random_string
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _
from django.conf import settings

from .managers import UserManager


GENDER_CHOICES = (
    ('male', 'Male'),
    ('female','Female'),
    ('other', 'Other'))



class User(AbstractUser):
    """User model."""

    username = None
    email = models.EmailField(_('email address'), unique=True)
    joindate=models.DateField(auto_now_add=True)
    uuid_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    phone_number = models.CharField(max_length=20,unique=True)
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
     
    



class County(models.Model):
    name = models.CharField(max_length=50)
    slug = models.SlugField(max_length=50, unique=True, blank=True)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(County, self).save(*args, **kwargs)

    def __str__(self):
        return self.name

class Town(models.Model):
    name = models.CharField(max_length=50)
    county = models.ForeignKey(County, on_delete=models.CASCADE)
    slug = models.SlugField(max_length=50, unique=True, blank=True)


    class Meta:
        verbose_name_plural = "Towns / Cities"


    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Town, self).save(*args, **kwargs)

    def __str__(self):
        return self.name


class Address(models.Model):
    user=models.ForeignKey(
        settings.AUTH_USER_MODEL,on_delete=models.CASCADE
        )
    full_name=models.CharField(max_length=100)
    post_code=models.CharField(max_length=100)
    address_line=models.CharField(max_length=100)
    address_line2=models.CharField(max_length=100)
    town_city=models.ForeignKey(
        Town,on_delete=models.CASCADE,
        related_name='town_city',null=True,blank=True)
    delivery_instructions=models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    default_address=models.BooleanField(default=False)

    class Meta:
        verbose_name = _("Address")
        verbose_name_plural = _("Addresses")


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

    
    def __str__(self):
        return self.full_name

class PickupStation(models.Model):
    name=models.CharField(max_length=100)
    address=models.CharField(max_length=100)
    phone_number=models.CharField(max_length=100)
    town=models.ForeignKey(Town,on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    default_station=models.BooleanField(default=False)


    class Meta: 
        verbose_name = _("Pickup Station")
        verbose_name_plural = _("Pickup Stations")
    
    def save(self, *args, **kwargs):
        if self.default_station:
            try:
                temp = PickupStation.objects.get(default_station=True)
                if self != temp:
                    temp.default_station = False
                    temp.save()
            except PickupStation.DoesNotExist:
                pass
        super(PickupStation, self).save(*args, **kwargs)
    
    