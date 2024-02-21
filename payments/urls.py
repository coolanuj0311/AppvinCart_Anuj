# urls.py

from django.urls import path
from . import views
from django.urls import path


urlpatterns = [
    path('payment_method/', views.add_payment_method, name='payment_method'),
    # path('confirm_payment/', views.confirm_payment, name='confirm_payment'),
    # path('handle_3d_secure/', views.handle_3d_secure, name='handle_3d_securet'),
    # # path('payment/', PayPageView.as_view() ,name='pay_page'),
   
]