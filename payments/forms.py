from django import forms


class MpesaNumberForm(forms.Form):
    phone_number=forms.IntegerField(
        widget=forms.NumberInput(attrs={'class':'form-control','placeholder':'2547xxxxxxxx'})
        
        
    )
    