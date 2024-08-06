import json
from django.http import Http404
import requests
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from authentication.serializers import ScheduleSerializer, UserRegistrationSerializer
from core.utils import ApiCustomResponse, get_user_object
from authentication.models import CustomUser, Schedule
from rest_framework.authtoken.models import Token
from rest_framework.permissions import AllowAny, IsAuthenticated


class UserRegistrationAPIView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            
            # Generate token for the user
            token, created = Token.objects.get_or_create(user=user)

            return Response(
                {
                    'status': True,
                    'status_code': status.HTTP_201_CREATED,
                    'response': {
                        'message': 'User Created Successfully',
                        'error_message': None,
                        'data': serializer.data,
                        'token': token.key
                    }
                },
                status=status.HTTP_201_CREATED
            )
        else:
            return Response(
                {
                    'status': False,
                    'status_code': status.HTTP_400_BAD_REQUEST,
                    'response': {
                        'message': 'Unable to Create User',
                        'error_message': str(serializer.errors)
                    }
                },
                status=status.HTTP_400_BAD_REQUEST
            )


class CheckUser(APIView, ApiCustomResponse):
    permission_classes = [AllowAny]

    def post(self, request):
        phone_number = request.data.get('phone_number', None)
        if phone_number is None:
            return self.get_response(
                message='Phone number is required.',
                status_code=status.HTTP_400_BAD_REQUEST,
            )
        # Normalize phone number
        # phone_number = ''.join(filter(str.isdigit, phone_number))
        
        # Perform case-insensitive lookup
        user = CustomUser.objects.filter(phone__iexact=phone_number).first()
        
        if user:
            token, created = Token.objects.get_or_create(user=user)
            data = {"token": token.key}
            return self.get_response(
                data=data,
                status_code=status.HTTP_200_OK,
            )
        else:
            return self.get_response(
                message='User does not exist with this phone number.',
                status_code=status.HTTP_404_NOT_FOUND,
            )


class Profile(APIView, ApiCustomResponse):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        # print("Request Headers:")
        # print(json.dumps(dict(request.headers), indent=4))
        # user = CustomUser.objects.get(user=request.user)
        serializer = UserRegistrationSerializer(request.user)
        return self.get_response(data=serializer.data)
    
    def put(self, request):
        serializer = UserRegistrationSerializer(request.user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return self.get_response(data=serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)   


class ChatCompletionView(APIView):
    def post(self, request):
        question = request.data.get("question")
        print(question)
        if not question:
            return Response({"error": "Question is required"}, status=status.HTTP_400_BAD_REQUEST)
        
        payload = {
            "model": "llama-3-sonar-small-32k-chat",
            "messages": [
                {
                    "role": "system",
                    "content": "Be precise and concise."
                },
                {
                    "role": "user",
                    "content": question
                }
            ]
        }
        headers = {
            "accept": "application/json",
            "content-type": "application/json",
            "Authorization": "Bearer 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" #f"Bearer {settings.API_KEY}"
        }
        try:
            response = requests.post("https://api.perplexity.ai/chat/completions", json=payload, headers=headers)
            response.raise_for_status()  # Raise an exception for HTTP errors
            response_data = response.json()  # Parse the JSON response
        except requests.exceptions.RequestException as err:
            return Response({"error": str(err)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        return Response(response_data, status=response.status_code)
    

class UserfcmTokenAPIView(APIView, ApiCustomResponse):
    permission_classes = [IsAuthenticated]

    def put(self, request, *args, **kwargs):
        fcm_token = request.GET.get('fcm_token', None)
        user_profile = request.user
        if fcm_token:
            user_profile.fcm_token=fcm_token
            user_profile.save()
            return self.get_response(
                message='Token Updated Successfully.',
                status_code=status.HTTP_200_OK,
            )
        else:
            return self.get_response(
                message='fcm_token field required.',
                status_code=status.HTTP_400_BAD_REQUEST,
            )
        

class ScheduleDetailAPIView(APIView, ApiCustomResponse):
    permission_classes = [IsAuthenticated]

    def get_object(self, pk):
        try:
            return Schedule.objects.get(pk=pk)
        except Schedule.DoesNotExist:
            raise Http404

    def get(self, request):
        user = request.user
        schedule = Schedule.objects.filter(user = user).first()
        serializer = ScheduleSerializer(schedule)
        return self.get_response(
                message=serializer.data,
                status_code=status.HTTP_200_OK,
            )

    def post(self, request):
        user = request.user
        schedule = Schedule.objects.filter(user=user).first()
        
        if schedule:
            # Update existing schedule
            serializer = ScheduleSerializer(schedule, data=request.data, partial=True, context={'request': request})
            if serializer.is_valid():
                serializer.save()
                return self.get_response(
                    message=serializer.data,
                    status_code=status.HTTP_200_OK,
                )
        else:
            # Create new schedule
            serializer = ScheduleSerializer(data=request.data, context={'request': request})
            if serializer.is_valid():
                serializer.save()
                return self.get_response(
                    message=serializer.data,
                    status_code=status.HTTP_201_CREATED,
                )
        
        return self.get_response(
            message=serializer.errors,
            status_code=status.HTTP_400_BAD_REQUEST,
        )
    

    def put(self, request):
        pk = request.data.get('id', None)
        schedule = self.get_object(pk)
        serializer = ScheduleSerializer(schedule, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request):
        pk = request.data.get('id', None)
        schedule = self.get_object(pk)
        serializer = ScheduleSerializer(schedule, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request):
        pk = request.data.get('id', None)
        schedule = self.get_object(pk)
        schedule.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)