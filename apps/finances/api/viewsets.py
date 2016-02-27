from django.utils import timezone

from rest_framework.response import Response
from rest_framework.decorators import detail_route

from apps.api.viewsets import BaseModelViewSet
from apps.finances.models import Invoice

from .serializers import InvoiceSerializer, InvoiceChargeSerializer


class InvoiceViewSet(BaseModelViewSet):
    serializer_class = InvoiceSerializer

    def get_queryset(self):
        return Invoice.objects.prefetch_related('campaigns').filter(
            company_id=self.request.session['company'])

    @detail_route(methods=['post'], url_path='charge')
    def charge(self, request, pk):
        invoice = Invoice.objects.get(id=pk)
        srlzr = InvoiceChargeSerializer(data=request.data)
        srlzr.klass = invoice
        srlzr.klass.attempted_on = timezone.now()
        # the actual charging takes place on the validator
        if srlzr.is_valid():
            invoice.campaigns.update(is_active=True)
            return Response(status=200)
        else:
            return Response(srlzr.errors, status=400)
