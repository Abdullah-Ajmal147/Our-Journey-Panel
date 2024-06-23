from django.urls import path
from authentication.views.v1.views import (
    UserRegistrationAPIView, 
    ChatCompletionView,
    CheckUser
    )

urlpatterns = [
    path('api/register/', UserRegistrationAPIView.as_view(), name='user-register'),
    path('api/checkuser/', CheckUser.as_view(), name='user-check'),
    path('api/test/', ChatCompletionView.as_view(), name='user-register'),



    # path('api/login/', UserLoginAPIView.as_view(), name='api-login'),
    # path('api/signup/', UserSignupAPIView.as_view(), name='api-signup'),
    # path('api/user/', GetUserView.as_view(), name='user-detail'),
    # path('api/login/', CustomAuthToken.as_view(), name='user-login'),
]
