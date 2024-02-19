from django.contrib import admin
from .models import Payment

admin.site.register(Payment)
# admin.py

from django.contrib import admin
from .models import StripeCustomer, PaymentMethod

@admin.register(StripeCustomer)
class StripeCustomerAdmin(admin.ModelAdmin):
    list_display = ('user', 'stripe_customer_id')
    search_fields = ('user__username', 'user__email', 'stripe_customer_id')
    # You can customize this further based on your needs

@admin.register(PaymentMethod)
class PaymentMethodAdmin(admin.ModelAdmin):
    list_display = ('customer', 'stripe_payment_method_id')
    search_fields = ('customer__user__username', 'customer__user__email', 'stripe_payment_method_id')