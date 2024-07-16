from django.db import models
from authentication.models import CustomUser
from django.core.validators import MinValueValidator, MaxValueValidator


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
    

class Review(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='User')
    rating = models.PositiveIntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Review by {self.user.username} - {self.rating} stars'
    

class Support(models.Model):
    STATUS_CHOICES = [
        ('open', 'Open'),
        ('in_progress', 'In Progress'),
        ('closed', 'Closed'),
    ]

    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='support_user')
    subject = models.CharField(max_length=255)
    description = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='open')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'Ticket {self.id} by {self.user.username} - {self.subject}'
    
