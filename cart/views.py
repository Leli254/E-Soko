from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from django.views.generic import View,DetailView

from shop.models import Product
from coupons.forms import CouponApplyForm

from .cart import Cart
from .forms import CartAddProductForm


@require_POST
def cart_add(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    form = CartAddProductForm(request.POST)
    if form.is_valid():
        cd = form.cleaned_data
        cart.add(product=product,
                 quantity=cd['quantity'],
                 override_quantity=cd['override'])
    return redirect('cart:cart_detail')


@require_POST
def cart_remove(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    cart.remove(product)
    return redirect('cart:cart_detail')


def cart_detail(request):
    cart = Cart(request)
    for item in cart:
        item['update_quantity_form'] = CartAddProductForm(initial={
                            'quantity': item['quantity'],
                            'override': True})
    coupon_apply_form = CouponApplyForm()
    return render(
        request, 
        'cart/detail.html', 
        {'cart': cart,
         'coupon_apply_form': coupon_apply_form})

#above view as class based view
class CartDetail(View):
    def get(self, request):
        cart = Cart(request)
        for item in cart:
            item['update_quantity_form'] = CartAddProductForm(initial={
                                'quantity': item['quantity'],
                                'override': True})
        coupon_apply_form = CouponApplyForm()
        return render(
            request, 
            'cart/detail.html', 
            {'cart': cart,
             'coupon_apply_form': coupon_apply_form})

#a class based view to add items to the cart without using a form
class CartAdd(View):
    def get(self, request, *args, **kwargs):
        product_id = self.kwargs['product_id']
        product = get_object_or_404(Product, id=product_id)
        cart = Cart(request)
        cart.add(product=product, quantity=1, override_quantity=False)
        return redirect('cart:cart_detail')