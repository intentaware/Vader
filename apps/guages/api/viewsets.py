from rest_framework.response import Response

from apps.api.permissions import PublisherAPIPermission
from apps.api.viewsets import BaseModelViewSet, ReporterViewSet
from .serializers import AssetSerializer, CreateAssetSerializer
from apps.guages.models import Asset, Metric

class AssetViewSet(BaseModelViewSet):
    serializer_class = AssetSerializer
    model = Asset

    def get_queryset(self):
        return Asset.objects.prefetch_related(
                    'metrics'
                ).filter(
                    publisher_id=self.request.session['company']
                )

    def create(self, request):
        data = request.data
        data['publisher'] = request.session['company']
        s = CreateAssetSerializer(data=data)
        if s.is_valid():
            asset = s.save()
            return Response(AssetSerializer(asset).data, status=201)
        else:
            return Response(s.errors, status=400)


class AssetReportViewSet(ReporterViewSet):
    permissions = (PublisherAPIPermission, )
    model = Asset
    reporter_model = Metric
    #lookup_field = 'key'
    serializer_class = AssetSerializer

    def not_implemented(self):
        return Response({
                'details': 'Not Available'
            }, status=403)

    def create(self, request, *args, **kwargs):
        return self.not_implemented()

    def list(self, request, *args, **kwargs):
        return self.not_implemented()

    def retrieve(self, request, *args, **kwargs):
        return self.not_implemented()

    def destroy(self, request, *args, **kwargs):
        return self.not_implemented()

    def update(self, request, *args, **kwargs):
        return self.not_implemented()

    def _filter(self, pk):
        obj = self.model.objects.get(key=pk)
        return {'{name}_id'.format(name=self.model._meta.model_name): obj.id}
