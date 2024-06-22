from rest_framework import status
from rest_framework.response import Response
from django.conf import settings


class ApiCustomResponse:
    def get_response(self, data=None, **kwargs):
        message = kwargs.get('message', 'Success')
        status_code = kwargs.get('status_code', status.HTTP_200_OK)

        response_data = {
            "status_code": status_code,
            "message": message,
            "data": data if data else dict()
        }
        return Response(data=response_data, status=status_code)