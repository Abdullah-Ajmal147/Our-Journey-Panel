from rest_framework import serializers
from authentication.serializers import UserRegistrationSerializer
from order.models import Location, Orders, Review, Support

class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = ['id', 'address', 'latitude', 'longitude']

class OrderSerializer(serializers.ModelSerializer):
    from_location = LocationSerializer()
    to_location = LocationSerializer()

    class Meta:
        model = Orders
        fields = ['id', 'from_location', 'to_location', 'ride_type', 'fare', 'payment_method', 'created_at', 'updated_at']

    def create(self, validated_data):
        from_location_data = validated_data.pop('from_location')
        to_location_data = validated_data.pop('to_location')
        from_location = Location.objects.create(**from_location_data)
        to_location = Location.objects.create(**to_location_data)
        order = Orders.objects.create(from_location=from_location, to_location=to_location, **validated_data)
        return order

    def update(self, instance, validated_data):
        from_location_data = validated_data.pop('from_location')
        to_location_data = validated_data.pop('to_location')

        instance.from_location.address = from_location_data.get('address', instance.from_location.address)
        instance.from_location.latitude = from_location_data.get('latitude', instance.from_location.latitude)
        instance.from_location.longitude = from_location_data.get('longitude', instance.from_location.longitude)
        instance.from_location.save()

        instance.to_location.address = to_location_data.get('address', instance.to_location.address)
        instance.to_location.latitude = to_location_data.get('latitude', instance.to_location.latitude)
        instance.to_location.longitude = to_location_data.get('longitude', instance.to_location.longitude)
        instance.to_location.save()

        instance.ride_type = validated_data.get('ride_type', instance.ride_type)
        instance.fare = validated_data.get('fare', instance.fare)
        instance.payment_method = validated_data.get('payment_method', instance.payment_method)
        instance.save()
        return instance
    

class ReviewSerializer(serializers.ModelSerializer):
    user = UserRegistrationSerializer()
    class Meta:
        model = Review
        fields = ['id', 'user', 'rating', 'comment', 'created_at']
        read_only_fields = ['created_at']


class SupportSerializer(serializers.ModelSerializer):
    class Meta:
        model = Support
        fields = ['id', 'user', 'subject', 'description', 'status', 'created_at', 'updated_at']
        read_only_fields = ['user', 'status', 'created_at', 'updated_at']