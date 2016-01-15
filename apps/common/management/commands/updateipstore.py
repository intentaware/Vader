from django.conf import settings
from django.core.management import BaseCommand
from django.apps import apps
from django.utils import timezone as _tz
from dateutil.relativedelta import *

class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        _delta = _tz.now() + relativedelta(months=-1)

        Impression = apps.get_model('impressions', 'impression')
        Metric = apps.get_model('guages', 'metric')
        IPStore = apps.get_model('warehouse', 'ipstore')

        queryset = Impression.objects.filter(
            meta__at_ip__isnull=False, meta__at_ip2geo__isnull=False)

        print queryset.count()

        for q in queryset:
            ip = q.meta['ip']
            try:
                location = q.meta['ip2geo']['location']

                store, created = IPStore.objects.get_or_create(ip=ip)

                if created:
                    print "Reverse geocoding against ip: %s" %(store.ip)
                    self.update_gecode(store, location)
                else:
                    if q.updated_on > _delta and store.updated_on < _delta:
                        if not (store.latitude == location['latitude'] and store.longitude == location['longitude']):
                            print "Updating reverse geocoding against ip: %s" %(store.ip)
                            self.update_gecode(store, location)
            except KeyError:
                pass

    def update_gecode(self, ip, location):
        from googlemaps import Client
        from django.conf import settings
        import json

        ip.latitude = location['latitude']
        ip.longitude = location['longitude']

        gmaps = Client(key=settings.GOOGLE_GEOCODE_KEY)
        result = gmaps.reverse_geocode((location['latitude'], location['longitude']))
        ip.geocode = json.dumps(result)

        ip.save()
