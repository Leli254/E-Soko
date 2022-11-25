from io import BytesIO
from xhtml2pdf import pisa

from django.views.generic import CreateView,DetailView,ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy 
from django.http import HttpResponse
from django.template.loader import get_template

from cart.cart import Cart

from .models import OrderItem,Order
from .forms import OrderCreateForm
from .tasks import order_created


class OrderCreateView(LoginRequiredMixin,CreateView):
    model = Order
    form_class = OrderCreateForm
    template_name = 'orders/create.html'
    success_url = reverse_lazy('payment:payment_type')
    login_url = reverse_lazy('users:login')

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
        return Order.objects.filter(user=self.request.user).exclude(order_status='cancelled')


class OrderDetailView(LoginRequiredMixin,DetailView):
    model=Order
    template_name='orders/detail.html'
    context_object_name='order'


class CancelledOrderListView(LoginRequiredMixin,ListView):
    '''
    a view to display a list of all cancelled orders
    '''
    model = Order
    template_name = 'orders/cancelled_list.html'
    context_object_name = 'orders'

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user,order_status='cancelled')


class CancelledOrderDetailView(LoginRequiredMixin,DetailView):
    '''
    a view to display details of a cancelled order
    '''
    model = Order
    template_name = 'orders/cancelled_detail.html'
    context_object_name = 'order'



def render_to_pdf(template_src, context_dict={}):
    template = get_template(template_src)
    html  = template
    result = BytesIO()
    pdf = pisa.pisaDocument(BytesIO(html.encode("ISO-8859-1")), result)
    if not pdf.err:
        return HttpResponse(result.getvalue(), content_type='application/pdf')
    return None



