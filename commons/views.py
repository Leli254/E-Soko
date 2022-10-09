from django.shortcuts import render
from django.urls import reverse, reverse_lazy
from django.views.generic import CreateView,DetailView,TemplateView,UpdateView



class ContactView(TemplateView):
    template_name = 'contact.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Contact'
        return context
