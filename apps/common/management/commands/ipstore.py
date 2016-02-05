from .companyimpressions import UnicodeWriter
from apps.warehouse.models import IPStore
from django.core.management import BaseCommand

class Command(BaseCommand):

    def handle(self, *args, **kwargs):
        queryset = IPStore.objects.filter(geocode__isnull=False)

        fieldnames = ['ip', 'latitude', 'longitude', 'long_postal_code',
            'nearest_address']

        with open('ipstore.csv', 'w') as csvfile:
            csvfile.write(u'\ufeff'.encode('utf8'))
            writer = UnicodeWriter(csvfile, fieldnames=fieldnames, extrasaction='ignore')
            writer.writeheader()

            for q in queryset:
                d = {
                    'ip': q.ip,
                    'latitude': q.latitude,
                    'longitude': q.longitude,
                    'long_postal_code': q.long_postal_code,
                    'nearest_address': q.nearest_address,
                }
                writer.writerow(d)
