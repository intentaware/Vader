import json

from rest_framework.exceptions import MethodNotAllowed
from rest_framework.authentication import BasicAuthentication
from rest_framework.response import Response

from apps.api.permissions import PublisherAPIPermission
from apps.api.mixins import BaseImpression
from apps.guages.models import Asset, Metric
from apps.users.models import Visitor


class PostMetric(BaseImpression):
    permission_classes = (PublisherAPIPermission, )
    authentication_classes = (BasicAuthentication, )

    def get(self, request, asset_id=None):
        raise MethodNotAllowed

    def post(self, request, asset_id=None):
        asset = Asset.objects.get(key=asset_id)
        meta = request.data.get('meta', dict())
        doc = self.process_request(request)
        if meta:
            meta = self.decode_base64(meta)
        doc.update(meta)
        visitor, created = Visitor.objects.get_or_create(key=request.visitor)
        metric = Metric.objects.create(
            asset=asset,
            visitor=visitor,
            meta=doc
            )
        return Response({'data': 'Success'}, status=201)
