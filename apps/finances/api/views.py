from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view

@api_view(['GET', 'POST'])
def invoice_webhook(request):
    print request.data
    return Response({}, status=200)
