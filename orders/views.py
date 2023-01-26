from io import BytesIO
from xhtml2pdf import pisa

from django.views.generic import CreateView,DetailView,ListView,FormView,TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy 
from django.http import HttpResponse,Http404
from django.template.loader import get_template


from cart.cart import Cart
from users.models import Address,PickupStation

from .models import OrderItem,Order
from .forms import OrderCreateForm,  PickupStationForm
from .tasks import order_created


class ConfirmShippingAddressView(LoginRequiredMixin,FormView):
    template_name = 'orders/shipping_address.html'
    form_class =  PickupStationForm
    success_url = reverse_lazy('orders:order_create')

    def form_valid(self, form):
        pickup_station = form.cleaned_data['pickup_station']
        self.request.session['pickup_station'] = pickup_station.id if pickup_station else None
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['cart'] = Cart(self.request)
        context['address'] = Address.objects.filter(user=self.request.user).first()
        return context


#a view to show cart items 
class OrderSummaryView(LoginRequiredMixin,TemplateView):
    template_name = 'orders/order_summary_sidebar.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['cart'] = Cart(self.request)
        return context


    
class OrderCreateView(LoginRequiredMixin,CreateView):
    model = Order
    form_class = OrderCreateForm
    template_name = 'orders/create.html'
    success_url = reverse_lazy('payment:payment_type')
    

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['request'] = self.request
        return kwargs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['cart'] = Cart(self.request)
        return context

    def form_valid(self, form):
        order = form.save(commit=False)
        order.user = self.request.user
        order.address = Address.objects.filter(user=self.request.user).first()
        pickup_station_id = self.request.session.get('pickup_station')
        if pickup_station_id:
            order.pickup_station = PickupStation.objects.get(id=pickup_station_id)
        cart = Cart(self.request)
        order.save()
        
        for item in cart:
            OrderItem.objects.create(order=order,
                                    product=item['product'],
                                    price=item['price'],
                                    quantity=item['quantity'])
        
        # clear the cart
        cart.clear()
        # launch asynchronous task to send an email
        order_created.delay(order.id)
        # set the order in the session
        self.request.session['order_id'] = order.id
        return super().form_valid(form)
    
    '''
    a method to redirect to different payment  pages depending on ,
    the payment type selected in the order create form
    '''
    def get_success_url(self):
        payment_type = self.request.POST.get('payment_method')
        if payment_type == 'mpesa_on_deliverly':
            return reverse_lazy('payment:mpesa_on_delivery')
        elif payment_type == 'via_card':
            return reverse_lazy('payment:stripe_payment_process')
        elif payment_type == 'bank_transfer':
            return reverse_lazy('payment:bank_transfer')
        else:
            return reverse_lazy('payment:get_mpesa_number')



class OrderListView(LoginRequiredMixin,ListView):
    model = Order
    template_name = 'orders/list.html'
    context_object_name = 'orders'

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user)
    
    
class OrderDetailView(LoginRequiredMixin,DetailView):
    model= Order
    template_name= 'orders/detail.html'
    context_object_name= 'order'
    
    
    def get_object(self, queryset=None):
        obj = super().get_object(queryset=queryset)
        if obj.user != self.request.user:
            raise Http404("Order not found or not accessible.")
        return obj

 
#a view to show list of orders a user has cancelled.   
class CancelledOrderListView(LoginRequiredMixin,ListView):
    model= Order
    template_name='orders/cancelled_list.html'

    
    def get_queryset(self):
        return Order.objects.filter(order_status='cancelled',user=self.request.user)
    
    
    
class CancelledOrderDetailView(LoginRequiredMixin,DetailView):
    model= Order
    template_name='orders/cancelled_detail.html'
    
    
    def get_object(self, queryset=None):
        obj = super().get_object(queryset=queryset)
        if obj.order_status != 'cancelled' or obj.user != self.request.user:
            raise Http404("Order not found or not accessible.")
        return obj
