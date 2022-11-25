import re

from django.shortcuts import render, redirect
from django.urls import reverse, reverse_lazy
from django.views.generic import CreateView,DetailView,TemplateView,UpdateView
from django.core.mail import send_mail, BadHeaderError
from django.http import HttpResponse, JsonResponse
from django.conf import settings


from .models import Subscriber
from .forms import ContactForm,FeedbackForm




class ContactView(CreateView):
	template_name = 'contact.html'
	form_class = ContactForm
	success_url = reverse_lazy('contact')

	def form_valid(self, form):
		form.save()
		return super().form_valid(form)

	def form_invalid(self, form):
		return super().form_invalid(form)

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['title'] = 'Contact Us'
		return context

	def send_mail(self, form):
		subject = form.cleaned_data['subject']
		from_email = form.cleaned_data['from_email']
		if subject and from_email:
			try:
				send_mail(subject, message, from_email, [''])
			except BadHeaderError:
				return HttpResponse('Invalid header found.')

class HomeView(TemplateView):
	template_name = 'home.html'

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['title'] = 'Home'
		return context

class ReturnPolicyView(TemplateView):
	template_name = 'return_policy.html'

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['title'] = 'Return Policy'
		return context



class NewsLetterView(CreateView):
	template_name = 'index.html'
	model = Subscriber
	fields = ['name','email']
	success_url = reverse_lazy('index')

	def form_valid(self, form):
		subject = 'NewsLetter Subscription'
		message = 'Hello ' + form.cleaned_data['name'] + ', Thanks for subscribing us. You will get notification of latest articles posted on our website. Please do not reply on this email.'
		email_from = settings.EMAIL_HOST_USER
		recipient_list = [form.cleaned_data['email'], ]
		send_mail(subject, message, email_from, recipient_list)
		return super().form_valid(form)


class EmailValidateView(DetailView):
	model = Subscriber
	template_name = 'index.html'
	context_object_name = 'email'

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['title'] = 'Email Validation'
		return context

	def get_object(self, *args, **kwargs):
		email = self.request.GET.get('email')
		if Subscriber.objects.filter(email=email).exists():
			res = JsonResponse({'msg': 'Email already exists'})
			return res
		else:
			res = JsonResponse({'msg': 'Email does not exists'})
			return res


class FeedbackView(CreateView):
	template_name = 'feedback.html'
	form_class = FeedbackForm
	success_url = reverse_lazy('feedback')

	def form_valid(self, form):
		form.save()
		return super().form_valid(form)

	def form_invalid(self, form):
		return super().form_invalid(form)

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['title'] = 'Feedback'
		return context

	def send_mail(self, form):
		subject = form.cleaned_data['subject']
		from_email = form.cleaned_data['from_email']
		if subject and from_email:
			try:
				send_mail(subject, message, from_email, [''])
			except BadHeaderError:
				return HttpResponse('Invalid header found.')