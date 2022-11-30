from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin
from django.utils.translation import gettext_lazy as _

from .models import User, Address,PickupStation

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
    list_display =  ['user','address_name','phone_number','additional_phone_number',]
    search_fields = ['user','address_name','phone_number','additional_phone_number',]
    ordering =  ['user','address_name','phone_number','additional_phone_number',]

admin.site.register(Address,AddressAdmin)


class PickupStationAdmin(admin.ModelAdmin):
    list_display = ['name','address','phone_number']
    search_fields = ['name','address','phone_number']
    ordering = ['name','address','phone_number']

admin.site.register(PickupStation,PickupStationAdmin)

