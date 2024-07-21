from rest_framework import serializers

from authentication.serializers import UserRegistrationSerializer
from common.models import FavoriteLocation, Review, Support
from authentication.models import CustomUser


class FavoriteLocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = FavoriteLocation
        fields = ['uuid', 'user', 'location_cord', 'address_name', 'created_at', 'updated_at', 'is_active']
        read_only_fields = ['user', 'created_at', 'updated_at']

    def create(self, validated_data):
        # Assuming 'user' is provided through request context
        user = self.context['request'].user
        return FavoriteLocation.objects.create(user=user, **validated_data)
    
class ReviewSerializer(serializers.ModelSerializer):
    user_review_by = serializers.PrimaryKeyRelatedField(queryset=CustomUser.objects.all())
    user_review_to = serializers.PrimaryKeyRelatedField(queryset=CustomUser.objects.all())

    class Meta:
        model = Review
        fields = ['uuid', 'user_review_by', 'user_review_to', 'rating', 'comment', 'created_at', 'updated_at', 'is_active']
        read_only_fields = ['created_at', 'updated_at']


class SupportSerializer(serializers.ModelSerializer):
    class Meta:
        model = Support
        fields = ['id', 'user', 'subject', 'description', 'status', 'created_at', 'updated_at']
        read_only_fields = ['user', 'status', 'created_at', 'updated_at']
