from django import forms
from django.utils.translation import gettext_lazy as _
from .models import Order
from users.models import Address,PickupStation
from shop.models import Coupon
from django.contrib.auth import get_user_model

#form to select a pickup station
class PickupStationForm(forms.Form):
    pickup_station = forms.ModelChoiceField(
        queryset=PickupStation.objects.all(),
        required=False,
        empty_label=_('Select a pickup station'),
    )



#a form to create an order
class OrderCreateForm(forms.ModelForm):

    class Meta:
        model = Order
        fields = ['payment_method', 'coupon']
        coupon=forms.ModelChoiceField(queryset=Coupon.objects.all(),required=False)
        labels = {
            'coupon': _('Coupon'),
            'payment_method': _('Payment Method'),
        }
        widgets = {
            'payment_method': forms.Select(attrs={'class': 'form-control'}),
        }


    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super(OrderCreateForm, self).__init__(*args, **kwargs)
        #self.fields['coupon'].queryset = Coupon.objects.filter(is_active=True).exclude(is_active=False)
          
        


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

   



    
    
   


