# models.py

from django.db import models
from accounted.models import User

class StripeCustomer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    stripe_customer_id = models.CharField(max_length=255)
    # Add any other fields related to your customer here

    def __str__(self):
        return f"{self.user.username}'s Stripe Customer"

class PaymentMethod(models.Model):
    customer = models.ForeignKey(StripeCustomer, on_delete=models.CASCADE)
    stripe_payment_method_id = models.CharField(max_length=255)
    # Add any other fields related to your payment method here

    def __str__(self):
        return f"Payment Method {self.id} of {self.customer.user.username}"
