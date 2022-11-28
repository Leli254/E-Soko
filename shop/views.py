from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse, reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import (
    DetailView,ListView,TemplateView,
    CreateView,UpdateView,DeleteView
)


from cart.forms import CartAddProductForm
from .models import Category, Product,Coupon,Wishlist
from .forms import VendorForm,ReviewForm



class ProductListView(ListView):
    model = Product
    template_name = 'shop/product/list.html'
    context_object_name = 'products'
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        return context

    def get_queryset(self):
        queryset = super().get_queryset()
        category_slug = self.kwargs.get('category_slug')
        if category_slug:
            category = get_object_or_404(Category, slug=category_slug)
            queryset = queryset.filter(category=category)
        return queryset
    


class ProductDetailView(DetailView):
    model = Product
    template_name = 'shop/product/detail.html'
    context_object_name = 'product'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['cart_product_form'] = CartAddProductForm()
        context['reviews']=self.object.reviews.all()
        return context
    
    

class ProductCreateView(LoginRequiredMixin, CreateView):
    model = Product
    fields = ['name', 'category', 'description', 'price', 'available', 'image']
    template_name = 'shop/product/create.html'
    success_url = reverse_lazy('shop:product_list')
    
    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)



class ProductUpdateView(LoginRequiredMixin, UpdateView):
    model = Product
    fields = ['name', 'category', 'description', 'price', 'available', 'image']
    template_name = 'shop/product/update.html'
    success_url = reverse_lazy('shop:product_list')
    
    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)


class ProductDeleteView(LoginRequiredMixin, DeleteView):
    model = Product
    template_name = 'shop/product/delete.html'
    success_url = reverse_lazy('shop:product_list')
    
    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(owner=self.request.user)


class ReviewCreateView(LoginRequiredMixin, CreateView):
    form_class=ReviewForm
    template_name = 'shop/review/create.html'
    success_url = reverse_lazy('shop:product_list')

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['product'] = Product.objects.get(id=self.kwargs['pk'])
        return context

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['product'] = Product.objects.get(id=self.kwargs['pk'])
        return kwargs

class ReviewUpdateView(LoginRequiredMixin, UpdateView):
    form_class=ReviewForm
    template_name = 'shop/review/update.html'
    success_url = reverse_lazy('shop:product_list')

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['product'] = Product.objects.get(id=self.kwargs['pk'])
        return context

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['product'] = Product.objects.get(id=self.kwargs['pk'])
        return kwargs


class CouponListView(LoginRequiredMixin,TemplateView):
    template_name = 'shop/coupon/list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['active_coupons']=Coupon.objects.filter(user=self.request.user,is_active=True)
        context['inactive_coupons']=Coupon.objects.filter(user=self.request.user,is_active=False)
        return context


#a view to  add a product to  wishlist
class AddToWishlistView(LoginRequiredMixin,TemplateView):
    template_name = 'shop/wishlist/add.html'

    ''' 
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['product'] = Product.objects.get(id=self.kwargs['pk'])
        return context
    '''

    def post(self, request, *args, **kwargs):
        product = Product.objects.get(id=self.kwargs['id'])
        product.wishlist.add(self.request.user)
        return redirect('shop:product_list')


#a view to  remove a product from wishlist
class RemoveFromWishlistView(LoginRequiredMixin,TemplateView):
    template_name = 'shop/wishlist/remove.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['product'] = Product.objects.get(id=self.kwargs['pk'])
        return context

    def post(self, request, *args, **kwargs):
        product = Product.objects.get(id=self.kwargs['pk'])
        product.wishlist.remove(self.request.user)
        return redirect('shop:product_list')

#a view to show wishlist
class WishlistView(LoginRequiredMixin,TemplateView):
    template_name = 'shop/wishlist/list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['wishlist']=Wishlist.objects.filter(user=self.request.user)
        return context