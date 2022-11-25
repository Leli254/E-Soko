from allauth.account.forms import SignupForm 
from django import forms 
from .models import User,Address

class CustomSignupForm(SignupForm):
    first_name = forms.CharField(max_length=30, label='First Name')
    last_name = forms.CharField(max_length=30, label='Last Name')
    phone_number = forms.CharField(max_length=30, label='Phone Number')
    
    
    def save(self,request):
        user = super(CustomSignupForm, self).save(request)
        
        first_name = self.cleaned_data['first_name']
        last_name = self.cleaned_data['last_name']
        phone_number = self.cleaned_data['phone_number']
       
        
        
        user.first_name = first_name
        user.last_name = last_name
        user.phone_number = phone_number
        
        
        user.save()
        return user
    

    
class AddressForm(forms.ModelForm):
   
    class Meta:
        model = Address
        fields = [
            'address_name','region','phone_number','additional_phone_number',
            'delivery_instructions','default_address'
            ]



        
    
class UpdateUserForm(forms.ModelForm):
    class Meta:
        model = User
        # Add here the fields you want to be present in the update form
        fields = ('first_name', 'last_name', 'email', 'phone_number')
        
        