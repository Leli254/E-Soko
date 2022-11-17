import uuid

from django.db import models
from django.urls import reverse
from django.conf import settings




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
    image = models.ImageField(upload_to='images/', blank=True)
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
    category = models.ForeignKey(Category,
                                 related_name='products',
                                 on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200)
    image = models.ImageField(upload_to='products/%Y/%m/%d',
                              blank=True)
    description = models.TextField(blank=True)
    price_before_discount = models.DecimalField(
        max_digits=10, decimal_places=2,blank=True, null=True)
    price = models.DecimalField(
        max_digits=10,decimal_places=2,verbose_name='Price after discount')
    available = models.BooleanField(default=True)
    stock = models.PositiveIntegerField(default=0)
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


    


class Review(models.Model):
    product=models.ForeignKey(Product, on_delete=models.CASCADE, related_name='reviews')
    user=models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='reviews')
    rating=models.IntegerField()
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