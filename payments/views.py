import datetime as dt
import json
from secrets import compare_digest
import requests
from requests.auth import HTTPBasicAuth
from decimal import Decimal
import stripe

from django.conf import settings
from django.db.transaction import atomic, non_atomic_requests
from django.http import HttpResponse ,HttpResponseForbidden ,JsonResponse
from django.views import View
from django.views.generic import CreateView,DetailView,TemplateView,UpdateView
from django.db import IntegrityError
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.utils.decorators import method_decorator
from django.shortcuts import render, redirect,reverse,get_object_or_404
from django.utils import timezone



from orders.models import Order
from . mpesa import MpesaAccessToken,LipaNaMpesaPassword
from .models import MpesaPayment
from .forms import MpesaNumberForm

#choose payment method view
class PaymentTypeView(TemplateView):
    template_name= 'payments/payment_type.html'


def getAccessToken(request):
    consumer_key = settings.MPESA_CONSUMER_KEY
    consumer_secret = settings.MPESA_CONSUMER_SECRET
    api_URL = settings.MPESA_API_URL

    r = requests.get(api_URL, auth=HTTPBasicAuth(consumer_key, consumer_secret))
    mpesa_access_token = json.loads(r.text)
    validated_mpesa_access_token = mpesa_access_token['access_token']

    return HttpResponse(validated_mpesa_access_token)

   
def get_mpesa_number(request):
    order_id = request.session.get('order_id', None)
    order = get_object_or_404(Order, id=order_id)


    if request.method == 'POST':
        
        form = MpesaNumberForm(request.POST)
        if form.is_valid():
            phone_number = form.cleaned_data['phone_number']
            request.session['phone_number'] = phone_number
            return redirect(reverse('payment:lipa_na_mpesa'))
    else:
        form = MpesaNumberForm()
    return render(request, 'payments/mpesa_number.html', {'form': form})



@csrf_exempt
@non_atomic_requests
def lipa_na_mpesa(request):
    order_id = request.session['order_id']
    order = get_object_or_404(Order, id=order_id)
    total_cost = order.get_total_cost()
    amount=float(total_cost)
    phone_number = request.session['phone_number']
    
    access_token = MpesaAccessToken.validated_mpesa_access_token
    '''
    if not compare_digest(access_token, ''): #we compare the access token to an empty string/invalid token
        return HttpResponseForbidden(
            'Invalid access token. Please generate a new one and try again.',
            content_type='text/plain'
        )
    '''

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
        "AccountReference": "Lyttis",
        "TransactionDesc": "Testing stk push"
    }

    response =requests.post(api_url, json=request, headers=headers)
    return JsonResponse(response.json())



@method_decorator(csrf_exempt, name='dispatch')
class MpesaStkPushCallbackView(View):
    def post(self, request):
        data = json.loads(request.body)['Body']['stkCallback']
        
        if data['ResultCode'] == 0:
            # if payment was successful
             try:
                with atomic():
                    MpesaPayment.objects.create(
                        MerchantRequestID=data['MerchantRequestID'],
                        CheckoutRequestID=data['CheckoutRequestID'],
                        ResultCode=data['ResultCode'],
                        ResultDesc=data['ResultDesc'],
                        Amount=data['CallbackMetadata']['Item'][0]['Value'],
                        MpesaReceiptNumber=data['CallbackMetadata']['Item'][1]['Value'],
                        Balance=data['CallbackMetadata']['Item'][2]['Value'],
                        TransactionDate=data['CallbackMetadata']['Item'][3]['Value'],
                        PhoneNumber=data['CallbackMetadata']['Item'][4]['Value'],
                    )
                    order_id = request.session['order_id']
                    order = get_object_or_404(Order, id=order_id)
                    order.paid = True
                    order.save()
                    return redirect(reverse('payment:payment_completed'))
             except IntegrityError:
                return HttpResponse('Payment already exists')

        return JsonResponse({"ResultCode": 0, "ResultDesc": "Success", "ThirdPartyTransID": 0})


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
               "ConfirmationURL": "https://8597-102-222-146-36.in.ngrok.io",
               "ValidationURL": "https://8597-102-222-146-36.in.ngrok.io"}
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


'''
def confirmation(request):
    response=lipa_na_mpesa(request)

    mpesa_body =request.body.decode('utf-8')
    mpesa_payment = json.loads(mpesa_body)
    mpesa_payment=json.loads(request.body)

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

'''


def payment_completed(request):
    return render(request, 'payments/completed.html')


def payment_canceled(request):
    return render(request, 'payments/canceled.html')

#for testing purposes
def lipa_na_mpesa_online(request):
    access_token = MpesaAccessToken.validated_mpesa_access_token
    api_url = "https://sandbox.safaricom.co.ke/mpesa/stkpush/v1/processrequest"
    headers = {"Authorization": "Bearer %s" % access_token}
    request = {
        "BusinessShortCode": LipaNaMpesaPassword.Business_short_code,
        "Password": LipaNaMpesaPassword.decode_password,
        "Timestamp": LipaNaMpesaPassword.lipa_time,
        "TransactionType": "CustomerPayBillOnline",
        "Amount": 1,
        "PartyA": 254712320768,  # replace with your phone number to get stk push
        "PartyB": LipaNaMpesaPassword.Business_short_code,
        "PhoneNumber": 254712320768,  # replace with your phone number to get stk push
        "CallBackURL": "https://sandbox.safaricom.co.ke/mpesa/",
        "AccountReference": "Soko",
        "TransactionDesc": "Testing stk push"
    }
    response = requests.post(api_url, json=request, headers=headers)
    return HttpResponse('success')

#Handle payment process using Stripe

# create the Stripe instance
stripe.api_key = settings.STRIPE_SECRET_KEY
#stripe.api_version = settings.STRIPE_API_VERSION


def stripe_payment_process(request):
    order_id = request.session.get('order_id', None)
    order = get_object_or_404(Order, id=order_id)

    if request.method == 'POST':
        success_url = request.build_absolute_uri(
                        reverse('payment:completed'))
        cancel_url = request.build_absolute_uri(
                        reverse('payment:canceled'))

        # Stripe checkout session data
        session_data = {
            'mode': 'payment',
            'client_reference_id': order.id,
            'success_url': success_url,
            'cancel_url': cancel_url,
            'line_items': []
        }
        # add order items to the Stripe checkout session
        for item in order.items.all():
            session_data['line_items'].append({
                'price_data': {
                    'unit_amount': int(item.price * Decimal('100')),
                    'currency': 'usd',
                    'product_data': {
                        'name': item.product.name,
                    },
                },
                'quantity': item.quantity,
            })

        # create Stripe checkout session
        session = stripe.checkout.Session.create(**session_data)

        # redirect to Stripe payment form
        return redirect(session.url, code=303)

    else:
        return render(request, 'payments/stripe_process.html', locals())

