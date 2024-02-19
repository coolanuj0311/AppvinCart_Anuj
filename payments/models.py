# models.py

from django.db import models
from accounted.models import User


class Payment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    payment_method_id = models.CharField(max_length=255)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Payment #{self.id} by {self.user.name}"

# models.py

from django.db import models
from accounted.models import User

class StripeCustomer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    stripe_customer_id = models.CharField(max_length=255)
    # Add any other fields related to your customer here

    def __str__(self):
        return f"{self.user.name}'s Stripe Customer"

class PaymentMethod(models.Model):
    customer = models.ForeignKey(StripeCustomer, on_delete=models.CASCADE)
    stripe_payment_method_id = models.CharField(max_length=255)
    # Add any other fields related to your payment method here

    def __str__(self):
        return f"Payment Method {self.id} of {self.customer.user.name}"