from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import View,DetailView

from shop.models import Product

from .cart import Cart
from .forms import CartAddProductForm

#a class based view to add single  to the cart on product list page
class CartAddSingleItem(View):
    def get(self, request, *args, **kwargs):
        product_id = self.kwargs['product_id']
        product = get_object_or_404(Product, id=product_id)
        cart = Cart(request)
        cart.add(product=product, quantity=1, override_quantity=False)
        return redirect('cart:cart_detail')


class CartAdd(View):
    def post(self, request, product_id):
        cart = Cart(request)
        product = get_object_or_404(Product, id=product_id)
        form = CartAddProductForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            cart.add(product=product,
                     quantity=cd['quantity'],
                     override_quantity=cd['override'])
        return redirect('cart:cart_detail')



class CartDetail(View):
    def get(self, request):
        cart = Cart(request)
        for item in cart:
            item['update_quantity_form'] = CartAddProductForm(initial={
                                'quantity': item['quantity'],
                                'override': True})
        return render(
            request, 
            'cart/detail.html', 
            {'cart': cart,})


class RemoveFromCart(View):
    def post(self, request, product_id):
        cart = Cart(request)
        product = get_object_or_404(Product, id=product_id)
        cart.remove(product)
        return redirect('cart:cart_detail')


