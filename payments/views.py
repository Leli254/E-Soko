import requests
from requests.auth import HTTPBasicAuth 
import json

from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from django.shortcuts import render, redirect,get_object_or_404
from django.urls import reverse

from . mpesa import MpesaAccessToken,LipaNaMpesaPassword
from orders.models import Order
from .models import MpesaPayment
from .forms import MpesaNumberForm




def getAccessToken(request):
    consumer_key = settings.MPESA_CONSUMER_KEY
    consumer_secret = settings.MPESA_CONSUMER_SECRET
    api_URL = settings.MPESA_API_URL

    r = requests.get(api_URL, auth=HTTPBasicAuth(consumer_key, consumer_secret))
    mpesa_access_token = json.loads(r.text)
    validated_mpesa_access_token = mpesa_access_token['access_token']

    return HttpResponse(validated_mpesa_access_token)

   
def get_mpesa_number(request):
    if request.method == 'POST':
        form = MpesaNumberForm(request.POST)
        if form.is_valid():
            phone_number = form.cleaned_data['phone_number']
            request.session['phone_number'] = phone_number
            return redirect(reverse('payment:lipa_na_mpesa'))
    else:
        form = MpesaNumberForm()
    return render(request, 'payments/mpesa_number.html', {'form': form})




def lipa_na_mpesa(request):
    order_id = request.session['order_id']
    order = get_object_or_404(Order, id=order_id)
    total_cost = order.get_total_cost()
    amount=float(total_cost)
    phone_number = request.session['phone_number']
    
    access_token = MpesaAccessToken.validated_mpesa_access_token
    api_url = "https://sandbox.safaricom.co.ke/mpesa/stkpush/v1/processrequest"
    headers = {"Authorization": "Bearer %s" % access_token}
    request = {
        "BusinessShortCode": LipaNaMpesaPassword.Business_short_code,
        "Password": LipaNaMpesaPassword.decode_password,
        "Timestamp": LipaNaMpesaPassword.lipa_time,
        "TransactionType": "CustomerPayBillOnline",
        "Amount": amount,
        "PartyA":phone_number, 
        "PartyB": LipaNaMpesaPassword.Business_short_code,
        "PhoneNumber":phone_number, 
        "CallBackURL": "https://sandbox.safaricom.co.ke/mpesa/",
        "AccountReference": "Soko",
        "TransactionDesc": "Testing stk push"
    }

    response = requests.post(api_url, json=request, headers=headers)
    return HttpResponse('success')


def payment_completed(request):
    return render(request, 'payments/completed.html')


def payment_canceled(request):
    return render(request, 'payments/canceled.html')

      

@csrf_exempt
def register_urls(request):
    access_token = MpesaAccessToken.validated_mpesa_access_token
    api_url = "https://sandbox.safaricom.co.ke/mpesa/c2b/v1/registerurl"
    headers = {"Authorization": "Bearer %s" % access_token}
    options = {"ShortCode": LipaNaMpesaPassword.Test_c2b_shortcode,
               "ResponseType": "Completed",
               "ConfirmationURL": "https://30bc-196-201-231-26.in.ngrok.io/payment/c2b/confirmation",
               "ValidationURL": "https://30bc-196-201-231-26.in.ngrok.io/payment/c2b/validation"}
    response = requests.post(api_url, json=options, headers=headers)

    return HttpResponse(response.text)


@csrf_exempt
def call_back(request):
    pass


@csrf_exempt
def validation(request):

    context = {
        "ResultCode": 0,
        "ResultDesc": "Accepted"
    }
    return JsonResponse(dict(context))


@csrf_exempt
def confirmation(request):
    mpesa_body =request.body.decode('utf-8')
    mpesa_payment = json.loads(mpesa_body)

    payment = MpesaPayment(
        first_name=mpesa_payment['FirstName'],
        last_name=mpesa_payment['LastName'],
        middle_name=mpesa_payment['MiddleName'],
        description=mpesa_payment['TransID'],
        phone_number=mpesa_payment['MSISDN'],
        amount=mpesa_payment['TransAmount'],
        reference=mpesa_payment['BillRefNumber'],
        organization_balance=mpesa_payment['OrgAccountBalance'],
        type=mpesa_payment['TransactionType'],

    )
    payment.save()

    context = {
        "ResultCode": 0,
        "ResultDesc": "Accepted"
    }

    return JsonResponse(dict(context))



def payment_completed(request):
    return render(request, 'payments/completed.html')


def payment_canceled(request):
    return render(request, 'payments/canceled.html')