"""
URL configuration for ecommerce project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include
from django.conf.urls.static import static
from django.conf import settings
from django.contrib import admin
from django.urls import path

from store import views
from django.contrib import admin
from django.urls import path
from payments.views import (
    CreateCheckoutSessionView,
    ProductLandingPageView,
    SuccessView,
    CancelView,
    stripe_webhook,
    StripeIntentView
)



urlpatterns = [
    path('admin/', admin.site.urls),
    path('',include('store.urls')),
    path('',include('accounted.urls')),
   
   
  
   
    path('',include('payments.urls')),
    path('create-payment-intent/<pk>/', StripeIntentView.as_view(), name='create-payment-intent'),
    path('webhooks/stripe/', stripe_webhook, name='stripe-webhook'),
    path('cancel/', CancelView.as_view(), name='cancel'),
    path('success/', SuccessView.as_view(), name='success'),
    path('', ProductLandingPageView.as_view(), name='landing-page'),
    path('create-checkout-session/<pk>/', CreateCheckoutSessionView.as_view(), name='create-checkout-session')

]
urlpatterns+=static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)


