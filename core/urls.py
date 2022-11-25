from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView


from commons import views as common_views


urlpatterns = [
    path('soko-admin/', admin.site.urls),
    path('common/', include('commons.urls')),
    path('users/', include('users.urls',namespace='users')),
    path('accounts/', include('allauth.urls')),
    path('accounts/profile/', TemplateView.as_view(template_name='support.html'),name='support'),
    path('help/',TemplateView.as_view(template_name='help.html'),name='help'),
    path('faqs/',TemplateView.as_view(template_name='faqs.html'),name='faqs'),
    #common urls
    path('contact/',common_views.ContactView.as_view(),name='contact'),
    path('return-policy/',common_views.ReturnPolicyView.as_view(),name='return_policy'),
    path('cart/', include('cart.urls',namespace='cart')),
    path('orders/', include('orders.urls',namespace='orders')),
    path('payment/', include('payments.urls', namespace='payment')),
    path('', include('shop.urls')),
]


if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)