from django.test import TestCase
from django.test.client import Client, RequestFactory
from django.urls.base import reverse

from .models import Contact, SubscribedUsers
from .views import ContactView, HomeView, NewsLetterView,EmailValidateView

'''
class ContactModelTest(TestCase):
    def test_saving_and_retrieving_items(self):
        first_contact = Contact()
        first_contact.first_name = 'John'
        first_contact.last_name = 'Doe'
        first_contact.email_address = 'joe@example.com'
        first_contact.message = 'Hello, I am John Doe'
        first_contact.save()

class ContactViewTest(TestCase):
    def test_redirects_after_POST(self):
        response = self.client.post(reverse('contact'), data={'first_name': 'John', 'last_name': 'Doe', 'email_address': '  ', 'message': 'Hello, I am John Doe'})
        self.assertEqual(response.status_code, 200) # 200 is the status code for a successful request
        self.assertTemplateUsed(response, 'contact.html')
        self.assertTrue(Contact.objects.exists())
'''