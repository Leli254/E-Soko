from django import forms
from django.utils.translation import gettext_lazy as _
from .models import Order
from users.models import Address,PickupStation
from shop.models import Coupon
#import request user below
from django.contrib.auth import get_user_model



class OrderCreateForm(forms.ModelForm):

    class Meta:
        model = Order
        fields = ['address','pickup_station','coupon','payment_method']
        labels = {
            'address': _('Address'),
            'pickup_station': _('Pickup Station'),
            'coupon': _('Coupon'),
            'payment_method': _('Payment Method'),
        }
        widgets = {
            'address': forms.RadioSelect(),
            'pickup_station': forms.Select(attrs={'class': 'form-control'}),
            'coupon': forms.CheckboxSelectMultiple(),
            'payment_method': forms.Select(attrs={'class': 'form-control'}),
        }


    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super(OrderCreateForm, self).__init__(*args, **kwargs)
        self.fields['address'].queryset = Address.objects.filter(user=self.request.user)
        self.fields['pickup_station'].queryset = PickupStation.objects.all()
        self.fields['coupon'].queryset = Coupon.objects.filter(
            user=self.request.user,is_active=True).exclude(is_active=False)
          
        


    def clean(self):
        cleaned_data = super(OrderCreateForm, self).clean()
        address = cleaned_data.get('address')
        pickup_station = cleaned_data.get('pickup_station')
        if address and pickup_station:
            raise forms.ValidationError(_
            ('You can only select either an address or a pickup station, not both'))
        if not address and not pickup_station:
            cleaned_data['address'] = Address.objects.get(user=self.request.user,default_address=True)
        return cleaned_data

   



    
    
   


