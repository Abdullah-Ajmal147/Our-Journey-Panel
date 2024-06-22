from rest_framework import serializers
from order.models import Orders

class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Orders
        fields = ['id', 'from_location', 'to_location', 'ride_type', 'fare', 'payment_method', 'created_at', 'updated_at']