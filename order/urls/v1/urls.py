from django.urls import path
from order.views.v1.views import OrderAPIView, ReviewAPIView

urlpatterns = [
    path('', OrderAPIView.as_view(), name='order-list-create'),
    path('reviews/', ReviewAPIView.as_view(), name='review-list-create'),
]