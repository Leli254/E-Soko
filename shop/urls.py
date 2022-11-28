from django.urls import path
from . import views

app_name = 'shop'

urlpatterns = [
    path('wishlist/', views.WishlistView.as_view(), name='wishlist'),
    path('wishlist/add/<int:id>/', views.AddToWishlistView.as_view(), name='wishlist_add'),
    path('wishlist/remove/<int:id>/', views.RemoveFromWishlistView.as_view(), name='wishlist_remove'),
    #path('<int:id>/<slug:slug>/add_review/', views.ReviewCreateView.as_view(), name='add_review'),
    path('coupon-list/', views.CouponListView.as_view(), name='coupon_list'),
    path('', views.ProductListView.as_view(), name='product_list'),
    path('<slug:category_slug>/', views.ProductListView.as_view(),name='product_list_by_category'),
    path('<int:id>/<slug:slug>/', views.ProductDetailView.as_view(),    name='product_detail'),
    path('create/', views.ProductCreateView.as_view(), name='product_create'),
]