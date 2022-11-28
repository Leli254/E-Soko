import uuid
from io import BytesIO
from PIL import Image

from django.core.files import File
from django.db import models
from django.urls import reverse
from django.conf import settings
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils import timezone




class Vendor(models.Model):
    name = models.CharField(max_length=100)
    owner=models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, 
        related_name='vendor', null=True, blank=True)
    slug = models.SlugField(max_length=100)
    description = models.TextField(blank=True)
    phone_number=models.CharField(max_length=15, blank=True, null=True)
    email=models.EmailField(blank=True, null=True)
    location=models.CharField(max_length=100,default='Nairobi')
    image = models.ImageField(upload_to='vendors/', blank=True)
    uuid_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('name',)
        verbose_name = 'vendor'
        verbose_name_plural = 'vendors'

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('shop:vendor_details', args=[self.slug])

class Category(models.Model):
    name = models.CharField(max_length=200)
    description=models.TextField(blank=True, null=True, default='')
    slug = models.SlugField(max_length=200,
                            unique=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    parent = models.ForeignKey(
        'self', blank=True, null=True,
        on_delete=models.CASCADE, related_name='children')
    is_featured = models.BooleanField(default=False)

    class Meta:
        ordering = ['name']
        indexes = [
            models.Index(fields=['name']),
        ]
        verbose_name = 'category'
        verbose_name_plural = 'categories'

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('shop:product_list_by_category',
                       args=[self.slug])


class Product(models.Model):
    SIZE_CHOICES = (
        ('S', 'Small'),
        ('M', 'Medium'),
        ('L', 'Large'),
        ('XL', 'Extra Large'),
        ('XXL', 'Extra Extra Large'),
    )

    category = models.ForeignKey(Category,
                                 related_name='products',
                                 on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200)
    image = models.ImageField(upload_to='products/%Y/%m/%d',null=True,blank=True)
    thumb_nail=models.ImageField(
        upload_to='products/%Y/%m/%d',null=True,blank=True)
    description = models.TextField(blank=True)
    #specifications
    in_the_box=models.CharField(max_length=100, blank=True, null=True)
    key_features = models.TextField(blank=True)
    sku = models.CharField(max_length=50, blank=True, null=True)
    model=models.CharField(max_length=100, blank=True, null=True)
    size_of_package = models.CharField(
        max_length=100, blank=True, null=True, choices=SIZE_CHOICES, default='S')
    product_size = models.CharField(
        max_length=100, blank=True, null=True,choices=SIZE_CHOICES, default='S')
    weight = models.DecimalField(
        max_digits=10, decimal_places=2,verbose_name='Weight (kg)',blank=True, null=True)
    main_material = models.CharField(max_length=100, blank=True, null=True)
    care_instructions = models.TextField(blank=True,verbose_name='Care Label',null=True)
    price_before_discount = models.DecimalField(
        max_digits=10, decimal_places=2,blank=True, null=True)
    price = models.DecimalField(
        max_digits=10,decimal_places=2,verbose_name='Price after discount')
    available = models.BooleanField(default=True)
    is_featured = models.BooleanField(default=False)
    stock = models.PositiveIntegerField(default=0)
    num_visits = models.IntegerField(default=0)
    last_visit = models.DateTimeField(blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    vendor=models.ForeignKey(
        Vendor,related_name='products',on_delete=models.CASCADE,blank=True,null=True)

    
    class Meta:
        ordering = ['name']
        indexes = [
            models.Index(fields=['id', 'slug']),
            models.Index(fields=['name']),
            models.Index(fields=['-created']),
        ]

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('shop:product_detail',
                       args=[self.id, self.slug])


    def get_thumbnail(self):
        if self.thumb_nail:
            return self.thumb_nail.url
        else:
            if self.image:
                self.thumbnail = self.make_thumbnail(self.image)
                self.save()
                
                return self.thumbnail.url
            else:
                return ''


    def make_thumbnail(self, image, size=(300, 300)):
        img = Image.open(image)
        img.convert('RGB')
        img.thumbnail(size)

        thumb_io = BytesIO()
        img.save(thumb_io, 'JPEG', quality=85)

        thumbnail = File(thumb_io, name=image.name)

        return thumbnail

class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='products/%Y/%m/%d')
    thumb_nail=models.ImageField(
        upload_to='products/%Y/%m/%d',null=True,blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['created']
        indexes = [
            models.Index(fields=['created']),
        ]

    def __str__(self):
        return self.product.name

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if self.image:
            img = Image.open(self.image.path)
            if img.height > 300 or img.width > 300:
                output_size = (300, 300)
                img.thumbnail(output_size)
                img.save(self.image.path)
    


class Review(models.Model):
    rate_choices=(
        (1,1),
        (2,2),
        (3,3),
        (4,4),
        (5,5),
        )
    product=models.ForeignKey(Product, on_delete=models.CASCADE, related_name='reviews')
    user=models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='reviews')
    rating=models.IntegerField(choices=rate_choices)
    comment=models.TextField(null=True, blank=True)
    created=models.DateTimeField(auto_now_add=True)
    updated=models.DateTimeField(auto_now=True)

    class Meta:
        ordering=['-created']

    def __str__(self):
        return f'{self.rating} review for {self.product.name}'

    def get_absolute_url(self):
        return reverse('shop:product_detail',
                       args=[self.product.id, self.product.slug])




class Coupon(models.Model):
    coupon_code = models.CharField(max_length=50, unique=True)
    valid_from = models.DateTimeField()
    valid_to = models.DateTimeField()
    value=models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)
    num_available = models.IntegerField(default=1)
    num_used = models.IntegerField(default=0)

    def __str__(self):
        return self.coupon_code
    

    def can_use(self):
        is_active = True

        if self.num_available <= self.num_used:
            is_active = False

        if self.valid_from > timezone.now():
            is_active = False

        if self.valid_to < timezone.now():
            is_active = False

        if self.is_active == False:
            is_active = False

        if self.num_used >= self.num_available and self.num_available != 0:
            is_active = False

        return is_active

    def use(self):
        self.num_used = self.num_used + 1
        if self.num_used >= self.num_available and self.num_available != 0:
            self.is_active = False
        self.save()
    
    #a method to deactivate a coupon if it has been used
    def deactivate(self):
        self.is_active = False
        self.save()


class Wishlist(models.Model):
    user=models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='wishlists')
    product=models.ForeignKey(Product, on_delete=models.CASCADE, related_name='wishlists')
    slug=models.SlugField(max_length=200,blank=True,null=True)
    created=models.DateTimeField(auto_now_add=True)
    updated=models.DateTimeField(auto_now=True)

    class Meta:
        ordering=['-created']

    def __str__(self):
        return f'{self.product.name} in {self.user.email} wishlist'

    def get_absolute_url(self):
        return reverse('shop:product_detail',
                       args=[self.product.id, self.product.slug])