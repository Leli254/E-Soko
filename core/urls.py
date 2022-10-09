from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView


from users.views import     (
    AddressCreateView, AddressListView, AddressUpdateView, AddressDeleteView,
)

urlpatterns = [
    path('soko-admin/', admin.site.urls),
    path('accounts/', include('allauth.urls')),
    path('accounts/address/create/', AddressCreateView.as_view(), name='address_create'),
    path('accounts/address/list/', AddressListView.as_view(), name='address_list'),
    path('accounts/address/update/<int:pk>/', AddressUpdateView.as_view(), name='address_update'),
    path('accounts/address/delete/<int:pk>/', AddressDeleteView.as_view(), name='address_delete'),
    path('',TemplateView.as_view(template_name='shop_base.html'),name='home'),
]
