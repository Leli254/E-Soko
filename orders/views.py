from io import BytesIO

from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import CreateView,DetailView,TemplateView,UpdateView,ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy,reverse  
from django.http import HttpResponse
from django.template.loader import get_template

from xhtml2pdf import pisa


from .models import OrderItem,Order
from .forms import OrderCreateForm
from .tasks import order_created
from cart.cart import Cart
from coupons.forms import CouponApplyForm



        
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
        context['coupon_apply_form'] = CouponApplyForm()
        return context

    def form_valid(self, form):
        order = form.save(commit=False)
        cart = Cart(self.request)
        order.save()
        
        for item in cart:
            OrderItem.objects.create(order=order,
                                    product=item['product'],
                                    price=item['price'],
                                    quantity=item['quantity'])
        
        # clear the cart
        cart.clear()
        # launch asynchronous task
        order_created.delay(order.id)
        # set the order in the session
        self.request.session['order_id'] = order.id
        return super().form_valid(form)
#write above class based view as function based view

def order_create(request):
    cart = Cart(request)
    if request.method == 'POST':
        form = OrderCreateForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            if cart.coupon:
                order.coupon = cart.coupon
                order.discount = cart.coupon.discount
            order.save()
            for item in cart:
                OrderItem.objects.create(order=order,
                                        product=item['product'],
                                        price=item['price'],
                                        quantity=item['quantity'])
            # clear the cart
            cart.clear()
            # launch asynchronous task
            order_created.delay(order.id)
            # set the order in the session
            request.session['order_id'] = order.id
            # redirect for payment
            return redirect(reverse('payment:payment_type'))
    else:
        form = OrderCreateForm()
    return render(request,
                'orders/create.html',
                {'cart': cart, 'form': form})


class OrderListView(LoginRequiredMixin,ListView):
    model = Order
    template_name = 'orders/list.html'
    context_object_name = 'orders'

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user)


def render_to_pdf(template_src, context_dict={}):
    template = get_template(template_src)
    html  = template
    result = BytesIO()
    pdf = pisa.pisaDocument(BytesIO(html.encode("ISO-8859-1")), result)
    if not pdf.err:
        return HttpResponse(result.getvalue(), content_type='application/pdf')
    return None



