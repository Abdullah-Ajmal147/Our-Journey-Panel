from django.db import models
from authentication.models import CustomUser
from core.utils import CoreModel


# Create your models here.
class FavoriteLocation(CoreModel):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='fav_user')
    location_cord = models.CharField(max_length=255, null=True, blank= True, verbose_name='cord_location')
    # from_location = models.CharField(max_length=255)
    address_name = models.CharField(max_length=255)

    def __str__(self):
        return self.address_name
