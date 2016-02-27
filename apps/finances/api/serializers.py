from rest_framework import serializers
from apps.finances.models import Invoice
from apps.api.serializers import StripeCreditCardSerializer
from apps.api.validators import StripeCardValidator
from apps.api.fields import ModelPropertyField


class InvoiceSerializer(serializers.ModelSerializer):
    line_items_total = ModelPropertyField()

    class Meta:
        model = Invoice


class InvoiceChargeSerializer(StripeCreditCardSerializer):
    class Meta:
        validators = [StripeCardValidator(klass='klass'), ]
