
from django.urls import path
from users.views import (AddressListView,AddressUpdateView, AddressDeleteView)

app_name = 'users'

urlpatterns = [
    #path('profile/', views.profile, name='profile'),
    #path('address/list/', AddressListView.as_view(), name='address_list'),
    #path('accounts/address/create/', AddressCreateView.as_view(), name='address_create'),
    path('address/update/<int:pk>/', AddressUpdateView.as_view(), name='address_update'),
    path('address/delete/<int:pk>/', AddressDeleteView.as_view(), name='address_delete'),
]
