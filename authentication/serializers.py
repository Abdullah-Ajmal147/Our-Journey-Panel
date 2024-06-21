from rest_framework import serializers
from .models import CustomUser

class UserRegistrationSerializer(serializers.ModelSerializer):

    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'phone', 'country_code', 'role', 'ride_category']

    def create(self, validated_data):
        user = CustomUser.objects.create_user(**validated_data)
        return user