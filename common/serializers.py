from rest_framework import serializers
from .models import FavoriteLocation

class FavoriteLocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = FavoriteLocation
        fields = ['uuid', 'user', 'location_cord', 'address_name', 'created_at', 'updated_at', 'is_active']
        read_only_fields = ['user', 'created_at', 'updated_at']

    def create(self, validated_data):
        # Assuming 'user' is provided through request context
        user = self.context['request'].user
        return FavoriteLocation.objects.create(user=user, **validated_data)
