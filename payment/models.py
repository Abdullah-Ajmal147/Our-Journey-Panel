# models.py
from django.db import models

class PaymentHistory(models.Model):
    payment_intent_id = models.CharField(max_length=255, unique=True)
    amount = models.IntegerField()
    currency = models.CharField(max_length=10)
    status = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    email = models.EmailField()

    def __str__(self):
        return f"{self.email} - {self.payment_intent_id} - {self.status}"
