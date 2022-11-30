from django.urls import path
from . import views

app_name = 'orders'

urlpatterns = [
    path('delivery-method/', views.ConfirmShippingAddressView.as_view(), name='delivery_method'),
    path('create/', views.OrderCreateView.as_view(), name='order_create'),
    path('list/', views.OrderListView.as_view(), name='my_orders'),
    path('list-cancelled/', views.CancelledOrderListView.as_view(), name='cancelled_orders'),
    path('cancelled-detail/<int:pk>/', views.CancelledOrderDetailView.as_view(),name='cancelled_order_detail'),
    path('orders/<int:pk>/', views.OrderDetailView.as_view(), name='order_detail'),

]