from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import MethodNotAllowed
from rest_framework.authentication import BasicAuthentication
from apps.api.permissions import PublisherAPIPermission

class PostMetric(APIView):
    permission_classes = (PublisherAPIPermission,)
    authentication_classes = (BasicAuthentication,)


    def get(self, request, asset_id=None):
        raise MethodNotAllowed(self.request.method)

    def post(self, request, asset_id=None):
        #print asset_id
        from apps.guages.models import Asset, Metric
        from apps.users.models import Visitor
        asset = Asset.objects.get(key=asset_id)
        meta = request.data.get('meta', dict())
        meta = self.process_base64(meta)
        backends = self.process_request(request)
        backends.update(meta)
        country = backends['ip2geo']['country']['iso_code']
        if country == 'US':
            from apps.warehouse.models import IPStore
            ip, created = IPStore.objects.get_or_create(ip=backends['ip'])
            if created or not ip.census:
                postal_code = backends['ip2geo']['postal']['code']
                census = Metric.get_census_data(postal_code)
                backends.update({
                    'census': census
                })
                ip.census = census
                ip.save()
            else:
                backends.update({
                    'census': ip.census
                })
        #print request.visitor
        visitor, created = Visitor.objects.get_or_create(key=request.visitor)
        Metric.objects.create(
            asset = asset,
            meta = backends,
            visitor = visitor
        )
        return Response()

    def process_base64(self, b64_string):
        import base64, json
        return json.loads(base64.b64decode(b64_string))

    def process_request(self, request):
        from ipware.ip import get_real_ip
        ip = get_real_ip(request) or '99.22.48.100'

        if ip:
            from geoip2 import database, webservice
            from django.conf import settings
            client = webservice.Client(
                settings.MAXMIND_CLIENTID, settings.MAXMIND_SECRET)
            ip2geo = client.insights(ip).raw
            #print ip2geo
            #reader = database.Reader(settings.MAXMIND_CITY_DB)
            #ip2geo = reader.city(ip).raw
        else:
            ip2geo = None
        user_agent = request.META['HTTP_USER_AGENT']
        return {
            'ip': ip,
            'user_agent': user_agent,
            'ip2geo': ip2geo,
        }

