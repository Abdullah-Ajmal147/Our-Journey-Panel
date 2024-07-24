from django.db import models
from authentication.models import CustomUser
from core.utils import CoreModel

# Create your models here.
class Location(models.Model):
    address = models.CharField(max_length=255)
    latitude = models.DecimalField(max_digits=20, decimal_places=16)
    longitude = models.DecimalField(max_digits=20, decimal_places=16)

    def __str__(self):
        return self.address
    

class Orders(CoreModel):
    RIDE_CHOICES = (
        ('ride_ac', 'Ride AC'),
        ('ride_mini', 'Ride Mini'),
        ('ride_x', 'Ride X'),
    )
    
    PAYMENT_METHOD_CHOICES = (
        ('cash', 'Cash'),
        ('credit_card', 'Credit Card'),
        ('paypal', 'PayPal'),
    )

    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
        ('canceled', 'Canceled'),
    )

    from_location = models.ForeignKey(Location, on_delete=models.CASCADE, related_name='from_orders')
    to_location = models.ForeignKey(Location, on_delete=models.CASCADE, related_name='to_orders')
    ride_type = models.CharField(max_length=50, choices=RIDE_CHOICES, default='ride_ac')

    fare = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    payment_method = models.CharField(max_length=50, choices=PAYMENT_METHOD_CHOICES, default='cash')
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='orders')
    captain_user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True, blank=True, related_name='captain_orders')

    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    payment_status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')

    estimated_duration = models.DurationField(null=True, blank=True)
    estimated_distance = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)

    def __str__(self):
        return f"{self.user.username} - {self.from_location.address} to {self.to_location.address}"

    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['user']),
            models.Index(fields=['created_at']),
            models.Index(fields=['status']),
        ]
