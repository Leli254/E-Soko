from django import forms
#import model form
from .models import Contact


# Create your forms here.

class ContactForm(forms.ModelForm):
	class Meta:
		model = Contact
		fields = ['first_name', 'last_name', 'email_address', 'message']