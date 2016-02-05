from django.db import models
from django_pgjson.fields import JsonBField
from django_extensions.db.fields import *

from apps.common.models import TimeStamped, IP2GeoModel


class Impression(TimeStamped, IP2GeoModel):
    campaign = models.ForeignKey('campaigns.Campaign', related_name='impressions')
    coupon = models.ForeignKey('campaigns.Coupon', related_name='impressions')
    #meta = JsonBField(blank=True, null=True)
    #visitor = models.ForeignKey('users.Visitor', related_name='impressions')
    publisher = models.ForeignKey('companies.Company', related_name='impressions')

    def create_from_request(self, request, campaign):
        from apps.users.models import Visitor
        self.campaign = campaign
        self.meta = request._request.META
        self.visitor, created = Visitor.objects.get_or_create(key=request.visitor)
        self.publisher = request.publisher
        pass

    def __unicode__(self):
        return '%s: %s' %(self.campaign, self.id)

    def _hydrate_meta(self):
        data = super(Impression, self)._hydrate_meta()
        data['coupon'] = self.coupon.code
        data['campaign'] = self.campaign.name
        return data

