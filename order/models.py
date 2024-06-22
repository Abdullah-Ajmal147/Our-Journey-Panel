from django.db import models
from authentication.models import CustomUser

# Create your models here.
class Orders(models.Model):
    RIDE_CHOICES = (
        ('RideAc', 'RideAc'),
        ('Echo', 'Echo'),
    )

    from_location = models.CharField(max_length=100)
    to_location = models.CharField(max_length=100)
    ride_type = models.CharField(max_length=50, choices=RIDE_CHOICES)
    fare = models.DecimalField(max_digits=10, decimal_places=2)
    payment_method = models.CharField(max_length=50)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='user')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username} - {self.from_location} to {self.to_location}"