from django.urls import path

from . import views
from .views import (
    MpesaStkPushCallbackView,MpesaNumberView,
    PayviaMpesaonDeliveryView,BankTransferView,PaymentCompletedView,
    PaymentCancelledView
    )

app_name = 'payment'

urlpatterns = [
    path('access/token', views.getAccessToken, name='get_mpesa_access_token'),
    path('online/lipa', views.lipa_na_mpesa_online, name='lipa_na_mpesa'),
    path('c2b/register', views.register_urls, name="register_mpesa_validation"),
    #path('c2b/confirmation', views.confirmation, name="confirmation"),
    path('c2b/validation', views.validation, name="validation"),
    path('c2b/callback', views.call_back, name="call_back"),
    path('mpesa-number/',MpesaNumberView.as_view(),name='get_mpesa_number'),
    path('lipa-na-mpesa/', views.lipa_na_mpesa, name='lipa_na_mpesa'),
    path('stk-push/callback/', MpesaStkPushCallbackView.as_view(), name='mpesa-stk-push-callback'),
    path('stripe-process/',views.stripe_payment_process,name='stripe_payment_process'),
    path('mpesa-on-deliverly/', PayviaMpesaonDeliveryView.as_view(), name='mpesa_on_delivery'),
    path('bank-transfer/', BankTransferView.as_view(), name='bank_transfer'),
    path('completed/', PaymentCompletedView.as_view(), name='completed'),
    path('cancelled/', PaymentCancelledView.as_view(), name='cancelled'),
]