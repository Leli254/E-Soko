from django.contrib import admin
from .models import Category, Product,Vendor,Review,Coupon,Wishlist


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'price',
                    'available', 'created', 'updated']
    list_filter = ['available', 'created', 'updated']
    list_editable = ['price', 'available']
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Vendor)
class VendorAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'description', 'image']
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ['product', 'user', 'rating', 'created', 'updated']
    list_filter = ['created', 'updated']
    list_editable = ['rating']


@admin.register(Coupon)
class CouponAdmin(admin.ModelAdmin):
    list_display = [
        'coupon_code', 'valid_from',
        'valid_to', 'value', 'is_active', 'num_available', 'num_used']
    list_filter = ['is_active', 'valid_from', 'valid_to']
    search_fields = ['coupon_code']


@admin.register(Wishlist)
class WishlistAdmin(admin.ModelAdmin):
    list_display = ['user', 'product', 'slug', 'created', 'updated']
    list_filter = ['created', 'updated']
    prepopulated_fields = {'slug': ('product',)}