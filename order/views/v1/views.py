from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from order.models import Orders
from order.serializers import OrderSerializer
from core.utils import ApiCustomResponse, get_user_object
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync


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
            'order_id': str(saved_instance.uuid),
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
    
    
class OrderStatusAPIView(APIView, ApiCustomResponse):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        status_list = ['pending', 'confirmed', 'in_progress']
        rides = Orders.objects.filter(user=request.user, status__in=status_list)
        serializer = OrderSerializer(rides, many=True)
        return self.get_response(data=serializer.data)
    
    
class ConfrimOrderAPIView(APIView, ApiCustomResponse):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        order_id = request.data.get('order_id', None)
        captain_id = request.data.get('captain_id', None)

        try:
            order = Orders.objects.filter(uuid=order_id).first()
            cap_id = get_user_object(captain_id)
            order.captain_user =cap_id
            order.status = 'confirmed'
            order.save()
            serializer = OrderSerializer(order)

            return self.get_response(
                data=serializer.data,
                status_code=status.HTTP_200_OK,
            )
        except Exception as e:
           return self.get_response(
            message=str(e),
            status_code=status.HTTP_400_BAD_REQUEST
        )