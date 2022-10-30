from django import forms
from django.utils.translation import gettext_lazy as _
from .models import Order
from users.models import Address,PickupStation
#import request user below
from django.contrib.auth import get_user_model



class OrderCreateForm(forms.ModelForm):

    class Meta:
        model = Order
        fields = ['address','pickup_station']


    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super().__init__(*args, **kwargs)
        self.fields['address'] = forms.ModelChoiceField(
            queryset=Address.objects.filter(user=self.request.user),
            empty_label=None,
            widget=forms.RadioSelect,
            required=False,
            label='Select Your Shipping Address'
        )
        self.fields['pickup_station'] = forms.ModelChoiceField(
            queryset=PickupStation.objects.all(),
            empty_label=None,
            #widget=forms.ChoiceField,
            required=False,
            label='Or Select Pickup Station'
        )

   



    
    
   


