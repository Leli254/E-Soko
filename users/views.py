from django.urls import reverse, reverse_lazy
from django.http import HttpResponseRedirect, HttpResponse, Http404
from django.shortcuts import get_object_or_404, render
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import (
    CreateView,DetailView,
    TemplateView,UpdateView,
    DeleteView,ListView
    )

from.models import Address,User
from .forms import AddressForm


class AddressCreateView(LoginRequiredMixin,CreateView):
    model = Address
    form_class = AddressForm
    template_name = 'users/address_form.html'
    success_url = reverse_lazy('users:address_list')
    
    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['addresses'] = Address.objects.filter(user=self.request.user)
        return context



class AddressListView(LoginRequiredMixin,TemplateView):
    template_name = 'users/address_list.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['addresses'] = Address.objects.filter(user=self.request.user)
        return context


class AddressUpdateView(LoginRequiredMixin,UpdateView):
    model = Address
    form_class = AddressForm
    template_name = 'users/address_form.html'
    success_url = reverse_lazy('users:address_list')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['addresses'] = Address.objects.filter(user=self.request.user)
        return context

class AddressDeleteView(LoginRequiredMixin,TemplateView):
    template_name = 'users/address_confirm_delete.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['address'] = Address.objects.get(pk=self.kwargs['pk'])
        return context
    
    def post(self, request, *args, **kwargs):
        address = get_object_or_404(Address, pk=self.kwargs['pk'])
        address.delete()
        return HttpResponseRedirect(reverse('users:address_list'))


class AddressDefaultView(LoginRequiredMixin,TemplateView):
    template_name = 'users/address_list.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['addresses'] = Address.objects.filter(user=self.request.user)
        return context
    
    def post(self, request, *args, **kwargs):
        address = get_object_or_404(Address, pk=self.kwargs['pk'])
        address.default = True
        address.save()
        return HttpResponseRedirect(reverse('users:address_list'))