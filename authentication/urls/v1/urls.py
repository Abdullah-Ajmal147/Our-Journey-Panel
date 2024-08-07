from django.urls import path
from authentication.views.v1.views import (
    ScheduleDetailAPIView,
    UserRegistrationAPIView, 
    ChatCompletionView, UserfcmTokenAPIView,
    CheckUser, Profile
    )

urlpatterns = [
    path('api/register/', UserRegistrationAPIView.as_view(), name='user-register'),
    path('api/checkuser/', CheckUser.as_view(), name='user-check'),
    path('api/profile/', Profile.as_view(), name='user-profile'),

    path('api/test/', ChatCompletionView.as_view(), name='user-register'),
    path('api/fcm-token/', UserfcmTokenAPIView.as_view(), name='fcm-token'),

    # Online status
    path('api/schedules/', ScheduleDetailAPIView.as_view(), name='schedule-detail'),

    # path('api/login/', UserLoginAPIView.as_view(), name='api-login'),
    # path('api/signup/', UserSignupAPIView.as_view(), name='api-signup'),
    # path('api/user/', GetUserView.as_view(), name='user-detail'),
    # path('api/login/', CustomAuthToken.as_view(), name='user-login'),
]
