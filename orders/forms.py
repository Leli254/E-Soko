from django import forms
from django.utils.translation import gettext_lazy as _
from .models import Order
from users.models import Address



class OrderCreateForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['address','pickup_station']




    address = forms.ModelChoiceField(
        
        widget=forms.RadioSelect,
        label='Select your shipping Address',
        queryset=Address.objects.all(),
        required=False
        )
    
    pickup_station = forms.ModelChoiceField(
        widget=forms.RadioSelect,
        label='Select your pickup station',
        queryset=Address.objects.all(),
        required=False
        )