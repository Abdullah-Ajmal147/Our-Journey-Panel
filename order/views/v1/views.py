from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from order.models import Orders, Review, Support
from order.serializers import OrderSerializer, ReviewSerializer, SupportSerializer
from core.utils import ApiCustomResponse
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from authentication.models import CustomUser


class OrderAPIView(APIView, ApiCustomResponse):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        rides = Orders.objects.filter(user=request.user)
        serializer = OrderSerializer(rides, many=True)
        return self.get_response(data=serializer.data)

    def post(self, request):
        serializer = OrderSerializer(data=request.data)
        if serializer.is_valid():
            saved_instance = serializer.save(user=request.user)

            # Websocket connection
            order_details = {
            'from_address': saved_instance.from_location.address,
            'from_latitude': str(saved_instance.from_location.latitude),
            'from_longitude': str(saved_instance.from_location.longitude),
            'to_address': saved_instance.to_location.address,
            'to_latitude': str(saved_instance.to_location.latitude),
            'to_longitude': str(saved_instance.to_location.longitude),
            'car_type': saved_instance.ride_type,
            'fare': str(saved_instance.fare),
            'order_id': saved_instance.id,
            'user_id': saved_instance.user_id,
            'user_name': request.user.name,
            'phone' : request.user.phone,
            'country_code': request.user.country_code,
            'email' : request.user.email,
            'role': request.user.role
            }

            layer = get_channel_layer()
            async_to_sync(layer.group_send)('online_captains', {
                'type': 'send_ride_order',
                'order_details': order_details
            })
            
            
            return self.get_response(
                data=serializer.data,
                status_code=status.HTTP_201_CREATED,
            )
        return self.get_response(
            message=serializer.errors,
            status_code=status.HTTP_400_BAD_REQUEST
        )
    
class ReviewAPIView(APIView, ApiCustomResponse):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        id = request.GET.get('id')
        reviews = Review.objects.filter(id = id).filter()
        serializer = ReviewSerializer(reviews, many=True)
        return self.get_response(
            data=serializer.data
        )

    def post(self, request):
        users = request.data.get('user', None)
        serializer = ReviewSerializer(data=request.data)
        if serializer.is_valid():
            user = get_object_or_404(CustomUser, id=users)
            serializer.save(user=user)#Wrequest.user)
            return self.get_response(
                data=serializer.data,
                status_code=status.HTTP_201_CREATED,
            )
        return self.get_response(
            message=serializer.errors,
            status_code=status.HTTP_400_BAD_REQUEST
        )

class TicketAPIView(APIView, ApiCustomResponse):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        tickets = Support.objects.filter(user=request.user)
        serializer = SupportSerializer(tickets, many=True)
        return self.get_response(
            data=serializer.data
        )

    def post(self, request):
        serializer = SupportSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return self.get_response(
                data=serializer.data,
                status_code=status.HTTP_201_CREATED,
            )
        return self.get_response(
            message=serializer.errors,
            status_code=status.HTTP_400_BAD_REQUEST
        )