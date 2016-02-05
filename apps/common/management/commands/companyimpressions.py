from django.conf import settings
from django.core.management import BaseCommand
import csv
import cStringIO
import codecs

class UnicodeWriter(object):

    def __init__(self, f, fieldnames, dialect=csv.excel, encoding="utf-8", **kwds):
        # Redirect output to a queue
        self.queue = cStringIO.StringIO()
        self.writer = csv.DictWriter(self.queue, fieldnames, dialect=dialect, **kwds)
        self.stream = f
        self.encoder = codecs.getincrementalencoder(encoding)()

    def writerow(self, D):
        try:
            self.writer.writerow({k:v.encode("utf-8", errors="replace") if isinstance(v, unicode) else v for k,v in D.items()})
        except UnicodeEncodeError:
            print "Unicode Error on"
            print D
        # Fetch UTF-8 output from the queue ...
        data = self.queue.getvalue()
        data = data.decode("utf-8")
        # ... and reencode it into the target encoding
        data = self.encoder.encode(data)
        # write to the target stream
        self.stream.write(data)
        # empty queue
        self.queue.truncate(0)

    def writerows(self, rows):
        for D in rows:
            self.writerow(D)

    def writeheader(self):
        self.writer.writeheader()



class Command(BaseCommand):

    def handle(self, *args, **kwargs):
        from apps.companies.models import Company
        from apps.impressions.models import Impression
        from apps.impressions.api.serializers import ImpressionCSVSerializer
        fieldnames = ['id', 'added_on', 'updated_on', 'visitor','ip', 'city',
            'postal_code', 'nearest_address', 'longitude', 'latitude', 'country',
            'user_agent', 'campaign', 'impression', 'coupon', 'publisher']
        for c in Company.objects.all():
            queryset = c.impressions.all().filter(meta__isnull=False, meta__at_ip__isnull=False)
            name = '%s.csv' %(c.name)
            with open(name, 'w') as csvfile:
                csvfile.write(u'\ufeff'.encode('utf8'))
                writer = UnicodeWriter(csvfile, fieldnames=fieldnames, extrasaction='ignore')
                writer.writeheader()
                for q in queryset:
                    meta = dict(q.hydrate_meta)
                    # serialized dict
                    q = dict(ImpressionCSVSerializer(q).data)
                    # merging two dictoinaries
                    meta.update(q)
                    writer.writerow(meta)
