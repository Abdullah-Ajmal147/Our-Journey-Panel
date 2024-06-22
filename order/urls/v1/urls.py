from django.urls import path
from order.views.v1.views import OrderAPIView

urlpatterns = [
    path('order/', OrderAPIView.as_view(), name='order-list-create'),
]