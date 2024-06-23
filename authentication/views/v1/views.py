import requests
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from authentication.serializers import UserRegistrationSerializer
from core.utils import ApiCustomResponse
from authentication.models import CustomUser
from rest_framework.authtoken.models import Token


class UserRegistrationAPIView(APIView):
    def post(self, request):
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            # return Response(
            #     serializer.data, 
            #     status=status.HTTP_201_CREATED)
        #return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            return Response(
                {
                    'status': True,
                    'status_code': status.HTTP_201_CREATED,
                    'response': {
                        'message': 'User Created Successfully',
                        'error_message': None,
                        'data': serializer.data,
                        # 'token': token.key
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
    def get(self, request):
        phone_number = request.data.get('phone_number', None)
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