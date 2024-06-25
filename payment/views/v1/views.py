from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from payment.serializers import CardInformationSerializer
import stripe
from django.conf import settings


class PaymentAPI(APIView):
    serializer_class = CardInformationSerializer

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        stripe.api_key = settings.STRIPE_SECRET_KEY

    def stripe_card_payment(self, data_dict):
        try:
            card_details = {
                "type": "card",
                "card": {
                    "number": data_dict['card_number'],
                    "exp_month": data_dict['expiry_month'],
                    "exp_year": data_dict['expiry_year'],
                    "cvc": data_dict['cvc'],
                },
            }
            
            # Create a PaymentIntent
            payment_intent = stripe.PaymentIntent.create(
                amount=10000,  # This is in the smallest currency unit (e.g., cents)
                currency='inr',
                payment_method_types=['card'],
            )

            # Modify the PaymentIntent with card details
            payment_intent_modified = stripe.PaymentIntent.modify(
                payment_intent['id'],
                payment_method=card_details['card'],
            )

            # Confirm the PaymentIntent
            payment_confirm = stripe.PaymentIntent.confirm(payment_intent['id'])
            
            # Retrieve the PaymentIntent to get its current status
            payment_intent_modified = stripe.PaymentIntent.retrieve(payment_intent['id'])

            if payment_intent_modified and payment_intent_modified['status'] == 'succeeded':
                response = {
                    'message': "Card Payment Success",
                    'status': status.HTTP_200_OK,
                    "card_details": card_details,
                    "payment_intent": payment_intent_modified,
                    "payment_confirm": payment_confirm
                }
            else:
                response = {
                    'message': "Card Payment Failed",
                    'status': status.HTTP_400_BAD_REQUEST,
                    "card_details": card_details,
                    "payment_intent": payment_intent_modified,
                    "payment_confirm": payment_confirm
                }
        except stripe.error.CardError as e:
            # Since it's a decline, stripe.error.CardError will be caught
            body = e.json_body
            err = body.get('error', {})
            response = {
                'error': err.get('message'),
                'status': status.HTTP_400_BAD_REQUEST,
                "payment_intent": {"id": "Null"},
                "payment_confirm": {'status': "Failed"}
            }
        except Exception as e:
            # Other errors will be caught here
            response = {
                'error': str(e),
                'status': status.HTTP_400_BAD_REQUEST,
                "payment_intent": {"id": "Null"},
                "payment_confirm": {'status': "Failed"}
            }
        
        return response

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        
        if serializer.is_valid():
            data_dict = serializer.validated_data
            response = self.stripe_card_payment(data_dict=data_dict)
        else:
            response = {'errors': serializer.errors, 'status': status.HTTP_400_BAD_REQUEST}

        return Response(response)
