from django.db import models
from django_extensions.db.fields import ShortUUIDField

from apps.common.models import TimeStamped, IP2GeoModel
# Create your models here.

class Asset(TimeStamped):
    name = models.CharField(max_length=128)
    url = models.URLField()
    key = ShortUUIDField()
    publisher = models.ForeignKey('companies.Company', related_name='assets')

    def __unicode__(self):
        return '%s - %s' %(self.url, self.publisher.name)


class Metric(TimeStamped, IP2GeoModel):
    asset = models.ForeignKey('guages.Asset', related_name='metrics')
