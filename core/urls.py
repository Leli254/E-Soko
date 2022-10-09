from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView


from users.views import AddressCreateView
from commons.views import ContactView


urlpatterns = [
    path('soko-admin/', admin.site.urls),
    path('users/', include('users.urls')),
    path('accounts/', include('allauth.urls')),
    path('accounts/profile/', AddressCreateView.as_view(), name='profile_create'),
    path('',TemplateView.as_view(template_name='home.html'),name='home'),
    path('help/',TemplateView.as_view(template_name='help.html'),name='help'),
    path('contact/',ContactView.as_view(),name='contact'),
]
