# locations/views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from common.models import FavoriteLocation
from common.serializers import FavoriteLocationSerializer
from django.http import Http404
from authentication.models import CustomUser
from core.utils import get_user_object


class FavoriteLocationAPIView(APIView):
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
        return Response(serializer.data)

    def post(self, request):
        data = request.data.copy()
        print(request.user.id)
        print(get_user_object(request.user.id))
        data['user'] = request.user.id
        print(data)
        serializer = FavoriteLocationSerializer(data=data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk):
        location = self.get_object(pk)
        data = request.data.copy()
        data['user'] = request.user.id
        serializer = FavoriteLocationSerializer(location, data=data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        location = self.get_fav_object(pk)
        location.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
