from rest_framework import serializers
from apps.finances.mixins import Stripe


class StripeSerializer(serializers.Serializer):
    """
    basic stripe serializer
    """
    amount = serializers.DecimalField(max_digits=20, decimal_places=4, required=True)
    description = serializers.CharField(max_length=256, required=True)


class StripeCreditCardSerializer(StripeSerializer):
    number = serializers.CharField(max_length=16, required=True)
    exp_year = serializers.IntegerField(required=True)
    exp_month = serializers.IntegerField(required=True)
    cvc = serializers.IntegerField(required=True)

    def get_source(self, cleaned_data):
        '''
        source is normally an invoice object, call be any other source i.e.
        Company
        '''
        source = cleaned_data
        del source['amount']
        del source['description']
        return source
