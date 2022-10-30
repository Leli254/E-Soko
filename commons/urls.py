from django.urls import path
from . import views

urlpatterns = [
    path('newsletter/', views.NewsLetterView.as_view(), name='newsletter'),
    path('validate/', views.EmailValidateView.as_view(), name='validate'),
]
