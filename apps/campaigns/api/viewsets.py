from rest_framework.response import Response
from rest_framework.decorators import detail_route, list_route

from apps.campaigns.models import Campaign
from apps.api.viewsets import BaseModelViewSet, ReporterViewSet
from .serializers import CampaignSerializer, CreateCampaignSerializer
from apps.impressions.models import Impression
from apps.impressions.api.serializers import ImpressionCSVSerializer


class CampaignViewSet(ReporterViewSet):
    serializer_class = CampaignSerializer
    prefetch_args = [
        'image',
        'coupons',
        'invoice',
        'coupons__impressions',
        'impressions',
    ]
    model = Campaign
    reporter_model = Impression

    def get_queryset(self):
        return super(CampaignViewSet, self).get_queryset()

    def create(self, request):
        data = request.data
        data['company'] = request.session['company']
        s = CreateCampaignSerializer(data=request.data)
        if s.is_valid():
            c = s.save()
            return Response(CampaignSerializer(c).data)
        else:
            return Response(s.errors, status=400)

    def update(self, request, *args, **kwargs):
        data = request.data
        instance = self.get_object()
        # print instance
        s = CreateCampaignSerializer(instance, data=data, partial=True)
        # print s
        if s.is_valid():
            self.perform_update(s)
            return Response(status=201)
        else:
            return Response(s.errors, 400)

    @list_route(methods=['get', ])
    def past(self, request, *args, **kwargs):
        return Response(
            CampaignSerializer(
                Campaign.objects.inactive(),
                many=True
            ).data,
            status=200
        )

