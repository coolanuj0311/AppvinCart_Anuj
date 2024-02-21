from django.db import models
from django.dispatch import receiver
from django.db.models.signals import post_save
from accounted.models import User

# Create your models here.
class Payment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    is_paid = models.BooleanField(default=False) #to determine if payment is done making or not
    client_secret = models.CharField(max_length=255)
    amount_paid = models.FloatField()
    