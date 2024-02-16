# urls.py

from django.urls import path
from . import views

urlpatterns = [
    
    path('payment_method/', views.payment_method, name='payment_method'),

    # Add more URL patterns as needed
]
