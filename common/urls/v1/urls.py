# locations/urls.py
from django.urls import path
from common.views.v1.views import FavoriteLocationAPIView, ReviewAPIView, TicketAPIView

urlpatterns = [
    path('fav-locations/', FavoriteLocationAPIView.as_view(), name='location-list-create'),
    path('locations/<uuid:pk>/', FavoriteLocationAPIView.as_view(), name='location-detail'),
    path('reviews/', ReviewAPIView.as_view(), name='review-list-create'),
    path('tickets/', TicketAPIView.as_view(), name='ticket-list-create'),
]
