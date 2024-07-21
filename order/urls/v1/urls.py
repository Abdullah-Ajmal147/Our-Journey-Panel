from django.urls import path
from order.views.v1.views import OrderAPIView, OrderStatusAPIView

urlpatterns = [
    path('', OrderAPIView.as_view(), name='order-list-create'),
    path('status/', OrderStatusAPIView.as_view(), name='order-status'),

]