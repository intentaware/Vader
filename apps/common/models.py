import logging
from django.db import models
from django_extensions.db.fields import CreationDateTimeField, \
    ModificationDateTimeField, AutoSlugField
from django.contrib.postgres.fields import JSONField

from .managers import BaseReportManager, BaseReportQuerySet

# Create your models here.

logger = logging.getLogger(__name__)


class BaseModel(models.Model):
    """
    Defines the basic model. The 'BaseModel' is the base model and is inherited
    everywhere.
    """

    def reload(self):
        """
        Reloads the object from the database
        """
        return self.__class__._default_manager.get(pk=self.pk)

    def has_foreign_key(self, name):
        """
        quickly check the 1to1 and FK rels where the model is not created.

        Args:
            name (str): represent the relationship name.

        Returns:
            (bool) or (object): either False or the desired object.

        Example:
            user = campaign.has_foreign_key('user')
        """
        return hasattr(self, name) and getattr(self, name) is not None

    class Meta:
        abstract = True


class TimeStamped(BaseModel):
    """
    Provides created and updated timestamps on models.
    This will be the model inherited site wide because for SAAS
    added_on and updated_on are required to check the action on
    a particular record
    """

    added_on = CreationDateTimeField()
    updated_on = ModificationDateTimeField()

    class Meta:
        abstract = True


class SluggedFromName(BaseModel):
    """
    Quickly provides a slug field and automate its creation from name
    """
    name = models.CharField(max_length=256)
    slug = AutoSlugField(populate_from='name', db_index=True)

    class Meta:
        abstract = True

    def __unicode__(self):
        return self.name


class SulggedFromTitle(BaseModel):
    """
    quickly provides a slug field and automate its creation from title
    """
    title = models.CharField(max_length=256)
    slug = AutoSlugField(populate_from='title', db_index=True)

    class Meta:
        abstract = True

    def __unicode__(self):
        return self.name


class ToCompany(BaseModel):
    """
    quickly creates a relationship to a company
    """
    company = models.ForeignKey(
        'companies.Company',
        blank=True,
        null=True,
        related_name='%(class)ss'
    )

    class Meta:
        abstract = True


class IP2GeoModel(BaseModel):
    meta = JSONField(blank=True, null=True)
    visitor = models.ForeignKey('users.visitor', related_name='%(class)ss')

    # custom manager
    objects = models.Manager()
    reporter = BaseReportManager.from_queryset(BaseReportQuerySet)()

    class Meta:
        abstract = True

    def _hydrate_meta(self):
        from django.apps import apps
        out = dict()
        out['id'] = self.id

        # clean garbage
        meta = self.meta
        meta.pop('meta', None)
        meta.pop('email', None)
        # flattening cascaded json
        ip2geo = meta.pop('ip2geo', None)
        nav = meta.pop('navigator', None)
        screen = meta.pop('screen', None)
        census = meta.pop('census', None)

        # inserting the remaining meta
        out.update(meta)

        if nav:
            for k, v in nav.iteritems():
                key = 'navigator_%s' % (k)
                out[key] = v

        if screen:
            for k, v in screen.iteritems():
                key = 'screen_%s' % (k)
                out[key] = v

        census_keys = ['age', 'education', 'job', 'transport', 'sex']

        if not census:
            census = dict()

        logger.info('census: %s' %(census))

        for k in census_keys:
            key = 'census_%s' % (k)
            value = census.get(k, '')
            logger.info('%s: %s' % (k, value))
            out[key] = value

        try:
            out['city'] = ip2geo['city']['names']['en'] if ip2geo else None
        except KeyError:
            out['city'] = None

        try:
            out['country'] = ip2geo['country']['names'][
                'en'
            ] if ip2geo else None
        except KeyError:
            out['country'] = None

        try:
            out['latitude'] = ip2geo['location'][
                'latitude'
            ] if ip2geo else None
        except KeyError:
            out['latitude'] = None

        try:
            out['longitude'] = ip2geo['location'][
                'longitude'
            ] if ip2geo else None
        except KeyError:
            out['longitude'] = None

        try:
            out['postal_code'] = ip2geo['postal']['code'] if ip2geo else None
        except KeyError:
            out['postal_code'] = None

        if ip2geo:
            traits = ip2geo['traits']
            for k, v in traits.iteritems():
                key = 'trait_%s' % (k)
                out[key] = v

        IPStore = apps.get_model('warehouse', 'IPStore')

        ip = out.get('ip', out.get('trait_ip_address', None))

        try:
            store = IPStore.objects.get(ip=ip)
        except IPStore.DoesNotExist:
            store = None

        out['nearest_address'] = store.nearest_address if store else None
        out['long_postal_code'] = store.long_postal_code if store else None

        return out

    @property
    def hydrate_meta(self):
        return self._hydrate_meta()

    def get_census_data(self):
        """
        Gets the census data against a given lookup

        Args:
            q (text): query string for text

        Returns:
            json: json for geo
        """
        from apps.warehouse.models import IPStore
        from plugins.census.models import Geography
        from plugins.census.api import CensusUS
        from plugins.census.ca import CaCensus

        census = None
        if self.meta:
            # first we will lookup the existing ipstore if it has data
            # then we will lookup the respective geographic census tables

            try:
                ip = self.meta['ip']
            except KeyError:
                ip = None

            try:
                warehouse = IPStore.objects.get(ip=ip)
                census = warehouse.census
            except IPStore.DoesNotExist:
                warehouse = IPStore.objects.create(ip=ip)

            if not census:
                try:
                    ip2geo = self.meta['ip2geo']
                except KeyError:
                    ip2geo = None

                if ip and ip2geo:
                    try:
                        country = ip2geo['country']['iso_code']
                    except KeyError:
                        country = None

                    try:
                        postcode = ip2geo['postal']['code']
                    except KeyError:
                        postcode = None

                    try:
                        city = ip2geo['city']['names']['en']
                    except KeyError:
                        city = None

                    try:
                        location = ip2geo['location']
                    except:
                        location = None

                    if country == 'US' and postcode:
                        queryset = IPStore.objects.filter(
                            geocoded_postal_code=postcode,
                            census__isnull=False
                        )
                        if queryset.count():
                            census = queryset[0].census
                        else:
                            try:
                                geoid = Geography.objects.get(
                                    full_name__contains=postcode
                                ).full_geoid.replace('|', '00US')
                                census = CensusUS(
                                    geoid=geoid
                                ).computed_profile()
                            except Geography.DoesNotExist:
                                print 'PostCode ID: %s' % (postcode)
                        warehouse.census = census
                        warehouse.save()

                    if country == 'Canada' and location:
                        from googlemaps import Client
                        from django.conf import settings

                        gmaps = Client(key=settings.GOOGLE_GEOCODE_KEY)
                        results = gmaps.reverse_geocode(
                            (location['latitude'], location['longitude'])
                        )
        return census

    def append_census_data(self):
        d = self.get_census_data()
        self.meta.update({'census': d})
        self.save()
