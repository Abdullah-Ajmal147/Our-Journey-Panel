# locations/views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from common.models import FavoriteLocation, Review, Support
from common.serializers import FavoriteLocationSerializer, ReviewSerializer, SupportSerializer
from django.http import Http404
from authentication.models import CustomUser
from core.utils import ApiCustomResponse, get_user_object


class FavoriteLocationAPIView(APIView, ApiCustomResponse):
    permission_classes = [IsAuthenticated]

    def get_fav_object(self, pk):
        try:
            return FavoriteLocation.objects.get(pk=pk, user=self.request.user)
        except FavoriteLocation.DoesNotExist:
            raise Http404

    def get(self, request, pk=None):
        if pk:
            location = self.get_fav_object(pk)
            serializer = FavoriteLocationSerializer(location)
        else:
            locations = FavoriteLocation.objects.filter(user=request.user)
            serializer = FavoriteLocationSerializer(locations, many=True)
        return self.get_response(data=serializer.data)

    def post(self, request):
        data = request.data.copy()
        data['user'] = request.user.id
        serializer = FavoriteLocationSerializer(data=data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return self.get_response(data=serializer.data, status_code=status.HTTP_201_CREATED)
        return self.get_response(data=serializer.errors, status_code=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk):
        location = self.get_object(pk)
        data = request.data.copy()
        data['user'] = request.user.id
        serializer = FavoriteLocationSerializer(location, data=data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return self.get_response(data=serializer.data)
        return self.get_response(data=serializer.errors, status_code=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        location = self.get_fav_object(pk)
        location.delete()
        return self.get_response(status_code=status.HTTP_204_NO_CONTENT)
    

class ReviewAPIView(APIView, ApiCustomResponse):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        id = request.GET.get('id')
        reviews = Review.objects.filter(user_review_to = id).filter()
        serializer = ReviewSerializer(reviews, many=True)
        return self.get_response(
            data=serializer.data
        )

    def post(self, request):
        data = request.data.copy()
        data['user_review_by'] = request.user.id
        user_review_to_id = request.data.get('user')
        
        if not CustomUser.objects.filter(id=user_review_to_id).exists():
            return self.get_response(
                message="User to be reviewed does not exist",
                status_code=status.HTTP_400_BAD_REQUEST
            )
        
        data['user_review_to'] = user_review_to_id
        data['is_active'] = True
        serializer = ReviewSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
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