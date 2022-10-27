from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin
from django.utils.translation import gettext_lazy as _

from .models import User, Address,PickupStation,County,Town


@admin.register(User)
class UserAdmin(DjangoUserAdmin):
    """Define admin model for custom User model without username."""

    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        (_('Personal info'), {'fields': ('first_name', 'last_name', 'phone_number',)}),
        (_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser',
                                       'groups', 'user_permissions')}),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2'),
        }),
    )
    list_display = ('email', 'first_name', 'last_name', 'is_staff')
    search_fields = ('email', 'first_name', 'last_name')
    ordering = ('email','first_name',)


class AddressAdmin(admin.ModelAdmin):
    list_display = ['user','full_name','post_code','address_line','address_line2','town_city']
    search_fields = ['user','full_name','post_code','address_line','address_line2','town_city']
    ordering = ['user','full_name','post_code','address_line','address_line2','town_city']

admin.site.register(Address,AddressAdmin)


class PickupStationAdmin(admin.ModelAdmin):
    list_display = ['name','address','phone_number']
    search_fields = ['name','address','phone_number']
    ordering = ['name','address','phone_number']

admin.site.register(PickupStation,PickupStationAdmin)

class CountyAdmin(admin.ModelAdmin):
    list_display = ['name','slug']
    search_fields = ['name','slug']
    ordering = ['name','slug']

admin.site.register(County,CountyAdmin)

class TownAdmin(admin.ModelAdmin):
    list_display = ['name','slug','county']
    search_fields = ['name','slug','county']
    ordering = ['name','slug','county']

admin.site.register(Town,TownAdmin)