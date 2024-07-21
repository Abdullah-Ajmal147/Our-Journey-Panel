from rest_framework import serializers
from .models import Message
from authentication.serializers import *

class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = '__all__'


class GetMessageSerializer(serializers.ModelSerializer):

    sender = UserRegistrationSerializer()
    receiver = UserRegistrationSerializer()
    class Meta:
        model = Message
        fields = '__all__'
