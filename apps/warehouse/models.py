from django.db import models

from apps.common.models import TimeStamped
from plugins.cities.models import PostalCode

from django.contrib.postgres.fields import JSONField


class IPStore(TimeStamped):
    ip = models.GenericIPAddressField(unpack_ipv4=True)
    # from existing django cities
    postal_code = models.ForeignKey('cities.PostalCode', blank=True, null=True)
    # from geocodes data
    geocoded_postal_code = models.CharField(max_length=8, blank=True, null=True)
    latitude = models.FloatField(blank=True, null=True)
    longitude = models.FloatField(blank=True, null=True)
    geocode = JSONField(blank=True, null=True)
    census = JSONField(blank=True, null=True)
    profile = JSONField(blank=True, null=True)

    def __unicode__(self):
        return self.ip

    @property
    def country(self):
        if self.postal_code:
            return self.postal_code.country.name
        else:
            return None

    @property
    def long_postal_code(self):
        pc = None
        if self.geocode:
            for s in self.geocode[0]['address_components']:
                try:
                    if s['types'][0] == 'postal_code':
                        # print self.ip
                        # print s
                        pc = s['long_name']
                except:
                    pass
        return pc

    @property
    def nearest_address(self):
        if self.geocode:
            return self.geocode[0]['formatted_address']
        else:
            return None




class PostalDemographics(TimeStamped):
    postal_code = models.ForeignKey('cities.PostalCode')
    income_per_capita = models.PositiveIntegerField(blank=True, null=True)
    income_household = models.PositiveIntegerField(blank=True, null=True)
