from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from order.models import Orders
from order.serializers import OrderSerializer
from core.utils import ApiCustomResponse


class OrderAPIView(APIView, ApiCustomResponse):
    # permission_classes = [IsAuthenticated]

    def get(self, request):
        rides = Orders.objects.filter(user=request.user)
        serializer = OrderSerializer(rides, many=True)
        # return Response(serializer.data, status=status.HTTP_200_OK)
        return self.get_response(data=serializer.data)

    def post(self, request):
        serializer = OrderSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            # return Response(serializer.data, status=status.HTTP_201_CREATED)
            return self.get_response(
                data=serializer.data,
                status_code=status.HTTP_201_CREATED,
                )
        return self.get_response(
                message=serializer.errors,
                status_code=status.HTTP_400_BAD_REQUEST
            )