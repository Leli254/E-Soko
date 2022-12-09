from django.urls import path
from . import views

app_name = 'cart'

urlpatterns = [
    path('', views.CartDetail.as_view(), name='cart_detail'),
    path('add/<int:product_id>/', views.CartAdd.as_view(), name='cart_add'),
    path('add-item/<int:product_id>/', views.CartAddSingleItem.as_view(), name='cart_add_single_item'),
    path('remove/<int:product_id>/',views.RemoveFromCart.as_view(),name='cart_remove'),
    
]
