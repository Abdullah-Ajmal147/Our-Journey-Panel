from django.urls import path
from order.views.v1.views import OrderAPIView

urlpatterns = [
    path('', OrderAPIView.as_view(), name='order-list-create'),
]