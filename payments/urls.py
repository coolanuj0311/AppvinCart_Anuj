# urls.py

from django.urls import path
from . import views

urlpatterns = [
    
    path('payment_method/', views.payment_method, name='payment_method'),
    path('process_payment/', views.process_payment, name='process_payment'),
   
    

    # Add more URL patterns as needed
]
