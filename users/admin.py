from allauth.account.forms import SignupForm 
from django import forms 
from .models import User,Profile,MedicProfile

class CustomSignupForm(SignupForm):
    first_name = forms.CharField(max_length=30, label='First Name')
    last_name = forms.CharField(max_length=30, label='Last Name')
    is_medic = forms.BooleanField(required=False,label='Are you a medic? Tick if yes')
    
    
    def save(self,request):
        user = super(CustomSignupForm, self).save(request)
        
        first_name = self.cleaned_data['first_name']
        last_name = self.cleaned_data['last_name']
        is_medic=self.cleaned_data['is_medic']
        
        
        user.first_name = first_name
        user.last_name = last_name
        user.is_medic = is_medic
        
        user.save()
        return user
    

    
class ProfileForm(forms.ModelForm):
    phone_number = forms.CharField(max_length=20, label='Phone Number')
    bio = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 5}))

    class Meta:
        model = Profile
        fields = ['phone_number','gender','avatar', 'bio','birthdate',]


class MedicProfileForm(forms.ModelForm):
    phone_number = forms.CharField(max_length=20, label='Phone Number')
    bio = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 5}))
    registration_number = forms.CharField(max_length=20, label='Registration Number')
    cadre = forms.CharField(max_length=20, label='Cadre')
    

    class Meta:
        model = MedicProfile
        fields = ['phone_number','gender','avatar', 'bio','birthdate','registration_number', 'cadre']
        
        
    
class UpdateUserForm(forms.ModelForm):
    class Meta:
        model = User
        # Add here the fields you want to be present in the update form
        fields = ('first_name', 'last_name','is_medic', 'email')
        
        
class ProfileUpdateForm(forms.ModelForm):
    bio = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 5}))
    
    class Meta:
        model = Profile
        fields=('avatar','bio','birthdate')