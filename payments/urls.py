# urls.py

from django.urls import path
from . import views
from django.urls import path
from payments.views import   CheckoutView, PaymentSuccessView, PayForCheckoutView

urlpatterns = [
    path('payment_method/', views.payment_method, name='payment_method'),
    # path('payment/', PayPageView.as_view() ,name='pay_page'),
    path('payment_success/',PaymentSuccessView.as_view(),name='successful_payment_page'),
    # path('payment_cancelled/',PaymentCancelledView.as_view(),name='failed-canceled_payment_page'),
    path('checkoutview/', views.CheckoutView, name='checkoutview'),
    path('pay_for_checkout/', views.PayForCheckoutView, name='pay_for_checkout'),  
]
