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
    is_medic = models.BooleanField(default=False)
    joindate=models.DateField(auto_now_add=True)
    uuid_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    

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
    
    def has_medicprofile(self):
        return hasattr(self, 'medicprofile')
    
    def has_profile(self):
        return hasattr(self, 'profile')
     
    
class Profile(models.Model):
    user=models.OneToOneField(
        settings.AUTH_USER_MODEL,on_delete=models.CASCADE
        )
    phone_number=models.CharField(max_length=20)
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES,default='Male')
    birthdate = models.DateField(null=True, blank=True)
    bio = models.TextField(default='', blank=True)
    avatar = models.ImageField(upload_to='profile_image', null=True, blank=True)
    slug = models.SlugField(max_length=255, unique=True, null=True, blank=True)
    uuid_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_verified = models.BooleanField(default=False)
    
    
    def __str__(self):  # __unicode__ for Python 2
        return self.user.email
    
    class Meta:
        verbose_name = _("User Profile")
        verbose_name_plural = _("User Profiles")
        
        
    def save(self, *args, **kwargs):
        slug = slugify(self.user.fullname)
        random_string = get_random_string(8, allowed_chars='abcdefghijklmnopqrstuvwxyz0123456789')
        self.slug = slug + "-" + random_string
        super().save(*args, **kwargs)
    
class MedicProfile(models.Model):
    user=models.OneToOneField(
        settings.AUTH_USER_MODEL,on_delete=models.CASCADE
        )
    phone_number=models.CharField(max_length=20)
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES,default='Male')
    birthdate = models.DateField(null=True, blank=True)
    bio = models.TextField(default='', blank=True)
    avatar = models.ImageField(upload_to='profile_image', null=True, blank=True)
    
    registration_number=models.CharField(max_length=20)
    cadre=models.CharField(max_length=20)
    slug = models.SlugField(max_length=255, unique=True, null=True, blank=True)
    uuid_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_verified = models.BooleanField(default=False)
    
    
    def __str__(self):  # __unicode__ for Python 2
        return self.user.email
    
    def save(self, *args, **kwargs):
        slug = slugify(self.user.fullname)
        random_string = get_random_string(8, allowed_chars='abcdefghijklmnopqrstuvwxyz0123456789')
        self.slug = slug + "-" + random_string
        super().save(*args, **kwargs)