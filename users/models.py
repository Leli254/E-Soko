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
     
    
class Address(models.Model):
    user=models.OneToOneField(
        settings.AUTH_USER_MODEL,on_delete=models.CASCADE
        )
    full_name=models.CharField(max_length=100)
    post_code=models.CharField(max_length=100)
    address_line=models.CharField(max_length=100)
    address_line2=models.CharField(max_length=100)
    town_city=models.CharField(max_length=100)
    delivery_instructions=models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    default_address=models.BooleanField(default=False)
    
    