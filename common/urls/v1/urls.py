# locations/urls.py
from django.urls import path
from common.views.v1.views import FavoriteLocationAPIView

urlpatterns = [
    path('fav-locations/', FavoriteLocationAPIView.as_view(), name='location-list-create'),
    path('locations/<uuid:pk>/', FavoriteLocationAPIView.as_view(), name='location-detail'),
]
