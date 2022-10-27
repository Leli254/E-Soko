from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView


from commons.views import contact


urlpatterns = [
    path('soko-admin/', admin.site.urls),
    path('users/', include('users.urls',namespace='users')),
    path('accounts/', include('allauth.urls')),
    path('accounts/profile/', TemplateView.as_view(template_name='support.html'),name='support'),
    path('',TemplateView.as_view(template_name='home.html'),name='home'),
    path('help/',TemplateView.as_view(template_name='help.html'),name='help'),
    path('faqs/',TemplateView.as_view(template_name='faqs.html'),name='faqs'),
    path('contact/',contact,name='contact'),
    path('cart/', include('cart.urls',namespace='cart')),
    path('orders/', include('orders.urls',namespace='orders')),
    path('payment/', include('payments.urls', namespace='payment')),
    path('shop/', include('shop.urls')),
]


if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)