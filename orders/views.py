from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import CreateView,DetailView,TemplateView,UpdateView,ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy,reverse    



from .models import OrderItem,Order
from .forms import OrderCreateForm
from .tasks import order_created
from cart.cart import Cart
from users.models import Address,PickupStation


class OrderCreateView(LoginRequiredMixin,CreateView):
    model = Order
    form_class = OrderCreateForm
    template_name = 'orders/create.html'
    success_url = reverse_lazy('orders:order_list')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['request'] = self.request
        return kwargs



    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['cart'] = Cart(self.request)
        return context

    def form_valid(self, form):
        response = super().form_valid(form)
        cart = Cart(self.request)
        for item in cart:
            OrderItem.objects.create(order=self.object,
                                    product=item['product'],
                                    price=item['price'],
                                    quantity=item['quantity'])
        # clear the cart
        cart.clear()
        # launch asynchronous task
        order_created.delay(self.object.id)
        # set the order in the session
        self.request.session['order_id'] = self.object.id
        # redirect for payment
        return redirect(reverse('payment:payment_type'))

    def get_success_url(self):
        return reverse('payment:payment_type')

class OrderListView(LoginRequiredMixin,ListView):
    model = Order
    template_name = 'orders/list.html'
    context_object_name = 'orders'

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user)