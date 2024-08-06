from rest_framework import serializers
from .models import CustomUser, Schedule

class UserRegistrationSerializer(serializers.ModelSerializer):

    class Meta:
        model = CustomUser
        fields = ['id','name', 'email', 'phone', 'country_code', 'role', 'ride_category']

    def create(self, validated_data):
        user = CustomUser.objects.create_user(**validated_data)
        return user
    

class ScheduleSerializer(serializers.ModelSerializer):

    class Meta:
        model = Schedule
        fields = ['id', 'user', 'online_status', 'start_time', 'end_time', 'route_start', 'route_end']
        read_only_fields = ['user']

    def create(self, validated_data):
        request = self.context.get('request')
        if request and hasattr(request, 'user'):
            validated_data['user'] = request.user
        return super().create(validated_data)

    def update(self, instance, validated_data):
        request = self.context.get('request')
        if request and hasattr(request, 'user'):
            validated_data['user'] = request.user
        return super().update(instance, validated_data)