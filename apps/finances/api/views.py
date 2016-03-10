from decimal import Decimal
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view

@api_view(['GET', 'POST'])
def invoice_webhook(request):
    data = request.data
    if 'payment_succeeded' in data['type']:
        invoice = data['data']['object']
        print invoice
        subscription = invoice['subscription']

    return Response({}, status=200)
