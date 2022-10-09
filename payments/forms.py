from django import forms


class MpesaNumberForm(forms.Form):
    phone_number=forms.IntegerField()
    