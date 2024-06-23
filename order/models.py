from django.db import models
from authentication.models import CustomUser

# Create your models here.
class Location(models.Model):
    address = models.CharField(max_length=255)
    latitude = models.DecimalField(max_digits=9, decimal_places=6)
    longitude = models.DecimalField(max_digits=9, decimal_places=6)

    def __str__(self):
        return self.address
    

class Orders(models.Model):
    RIDE_CHOICES = (
        ('ride_ac', 'ride_ac'),
        ('ride_mini', 'ride_mini'),
        ('ride_x', 'ride_x'),
    )

    from_location = models.ForeignKey(Location, on_delete=models.CASCADE, related_name='from_orders')
    to_location = models.ForeignKey(Location, on_delete=models.CASCADE, related_name='to_orders')
    ride_type = models.CharField(max_length=50, choices=RIDE_CHOICES)
    fare = models.DecimalField(max_digits=10, decimal_places=2)
    payment_method = models.CharField(max_length=50)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='user')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username} - {self.from_location} to {self.to_location}"
    
