from django.db import models
from authentication.models import CustomUser
from core.utils import CoreModel
from django.core.validators import MinValueValidator, MaxValueValidator


# Create your models here.
class FavoriteLocation(CoreModel):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='fav_user')
    location_cord = models.CharField(max_length=255, null=True, blank= True, verbose_name='cord_location')
    # from_location = models.CharField(max_length=255)
    address_name = models.CharField(max_length=255)

    def __str__(self):
        return self.address_name
    
class Review(CoreModel):
    user_review_by = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, blank=True, related_name='user_review_by')
    user_review_to = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='user_review_to')
    rating = models.PositiveIntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    comment = models.TextField()

    def __str__(self):
        return f'Review by {self.user_review_to.username} - {self.rating} stars'
    

class Support(CoreModel):
    STATUS_CHOICES = [
        ('open', 'Open'),
        ('in_progress', 'In Progress'),
        ('closed', 'Closed'),
    ]

    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='support_user')
    subject = models.CharField(max_length=255)
    description = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='open')

    def __str__(self):
        return f'Ticket {self.id} by {self.user.username} - {self.subject}'
