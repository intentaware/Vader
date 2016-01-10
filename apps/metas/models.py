from django.db import models
from apps.common.models import *

class Circle(TimeStamped):
    parent = models.ForeignKey('self', blank=True, null=True, related_name="children")
    name = models.CharField(max_length=64)

    def __unicode__(self):
        return self.name

class PublisherCircle(TimeStamped):
    publisher = models.ForeignKey('companies.Company')
    circle = models.ForeignKey('metas.Circle')
    is_active = models.BooleanField(default=True)

    class Meta:
        unique_together=['publisher', 'circle']


class CampaignCircle(TimeStamped):
    campaign = models.ForeignKey('campaigns.Campaign')
    circle = models.ForeignKey('metas.Circle')
    is_active = models.BooleanField(default=True)

    class Meta:
        unique_together = ['campaign', 'circle']


class CampaignCity(TimeStamped):
    campaign = models.ForeignKey('campaigns.Campaign')
    circle = models.ForeignKey('cities.City')
    is_active = models.BooleanField(default=True)

    class Meta:
        unique_together = ['campaign', 'circle']

class DomainData(TimeStamped):
    domain = models.CharField(max_length=255, unique=True)

class ScrapedData(TimeStamped):
    domain = models.ForeignKey(DomainData)
    url = models.TextField(null=True, blank=True)
    jsondata = models.TextField(null=True, blank=True)

