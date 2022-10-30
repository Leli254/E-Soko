from django.contrib import admin

from .models import SubscribedUsers, Contact

admin.site.register(SubscribedUsers)
admin.site.register(Contact)

