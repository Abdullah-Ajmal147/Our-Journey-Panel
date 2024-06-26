# views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.conf import settings
import stripe
from payment.serializers import TokenPaymentSerializer
from payment.models import PaymentHistory

class PaymentAPI(APIView):
    serializer_class = TokenPaymentSerializer

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        stripe.api_key = settings.STRIPE_SECRET_KEY

    def stripe_token_payment(self, data_dict):
        try:
            # Create a PaymentIntent
            payment_intent = stripe.PaymentIntent.create(
                amount=10000,  # This is in the smallest currency unit (e.g., cents)
                currency='inr',
                payment_method_data={
                    'type': 'card',
                    'card': {'token': data_dict['stripeToken']}
                },
                confirm=True
            )

            # Log payment attempt
            payment_log = PaymentHistory.objects.create(
                payment_intent_id=payment_intent['id'],
                amount=payment_intent['amount'],
                currency=payment_intent['currency'],
                status=payment_intent['status'],
                email=data_dict['email']
            )

            if payment_intent and payment_intent['status'] == 'succeeded':
                response = {
                    'message': "Card Payment Success",
                    'status': status.HTTP_200_OK,
                    "payment_intent": payment_intent
                }
            else:
                response = {
                    'message': "Card Payment Failed",
                    'status': status.HTTP_400_BAD_REQUEST,
                    "payment_intent": payment_intent
                }
        except stripe.error.CardError as e:
            # Since it's a decline, stripe.error.CardError will be caught
            body = e.json_body
            err = body.get('error', {})

            # Log failed payment attempt
            payment_log = PaymentHistory.objects.create(
                payment_intent_id='Null',
                amount=10000,  # Log the intended amount
                currency='inr',
                status='failed',
                email=data_dict['email']
            )

            response = {
                'error': err.get('message'),
                'status': status.HTTP_400_BAD_REQUEST,
                "payment_intent": {"id": "Null"}
            }
        except Exception as e:
            # Other errors will be caught here

            # Log failed payment attempt
            payment_log = PaymentHistory.objects.create(
                payment_intent_id='Null',
                amount=10000,  # Log the intended amount
                currency='inr',
                status='failed',
                email=data_dict['email']
            )

            response = {
                'error': str(e),
                'status': status.HTTP_400_BAD_REQUEST,
                "payment_intent": {"id": "Null"}
            }

        return response

    def post(self, request):
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            data_dict = serializer.validated_data
            response = self.stripe_token_payment(data_dict=data_dict)
        else:
            response = {'errors': serializer.errors, 'status': status.HTTP_400_BAD_REQUEST}

        return Response(response)
