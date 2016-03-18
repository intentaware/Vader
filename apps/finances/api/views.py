from decimal import Decimal
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from apps.companies.models import CompanySubscription
from apps.finances.models import Invoice
from django.utils import timezone as _tz


@api_view(['GET', 'POST'])
def invoice_webhook(request):
    data = request.data
    if 'payment_succeeded' in data['type']:
        invoice = data['data']['object']
        # subscription = invoice['subscription']
        try:
            subscription = CompanySubscription.objects.get(
                stripe_id=invoice['subscription']
            )
        except CompanySubscription.DoesNotExist:
            subscription = None
        # amount from stripe comes as type(str) and is in cents, we need to convert it to
        # type(Decimal) and dollars.cents
        amount = Decimal[invoice['total']] / 100
        now = _tz.now()
        if subscription:
            Invoice.objects.create(
                stripe_id=invoice['id'],
                company=subscription.company,
                amount=amount,
                attempts=invoice['attempt_count'],
                attempted_on=now,
                charged_on=now,
                gateway_response=data,
                is_paid=True
            )
            return Response({}, status=201)
        else:
            return Response({
                    'message': 'No subscription for this subscription exists'
                }, status=200)

    return Response({}, status=200)
