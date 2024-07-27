from django.urls import path
from order.views.v1.views import (
    ConfrimOrderAPIView, OrderAPIView, OrderStatusAPIView,
)

urlpatterns = [
    path('', OrderAPIView.as_view(), name='order-list-create'),
    path('status/', OrderStatusAPIView.as_view(), name='order-status'),
    path('confrim-order/', ConfrimOrderAPIView.as_view(), name='confrim-order'),
]