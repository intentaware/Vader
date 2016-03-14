from django.db import models
from django_extensions.db.fields import CreationDateTimeField, \
    ModificationDateTimeField, AutoSlugField
from django.contrib.postgres.fields import JSONField

# Create your models here.


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
    company = models.ForeignKey('companies.Company',
                                blank=True,
                                null=True,
                                related_name='%(class)ss')

    class Meta:
        abstract = True


class IP2GeoModel(BaseModel):
    meta = JSONField(blank=True, null=True)
    visitor = models.ForeignKey('users.visitor', related_name='%(class)ss')

    class Meta:
        abstract = True

    def _hydrate_meta(self):
        from django.apps import apps
        out = dict()
        out['id'] = self.id
        out['visitor'] = self.visitor.key

        # clean garbage
        meta = self.meta
        meta.pop('meta', None)
        meta.pop('email', None)

        # flattening cascaded json
        ip2geo = meta.pop('ip2geo', None)
        nav = meta.pop('navigator', None)
        screen = meta.pop('screen', None)

        if nav:
            for k, v in nav.iteritems():
                key = 'navigator_%s' % (k)
                out[key] = v

        if screen:
            for k, v in screen.iteritems():
                key = 'screen_%s' % (k)
                out[key] = v

        try:
            out['city'] = ip2geo['city']['names']['en'] if ip2geo else None
        except KeyError:
            out['city'] = None

        try:
            out['country'] = ip2geo['country']['names'][
                'en'] if ip2geo else None
        except KeyError:
            out['country'] = None

        try:
            out['latitude'] = ip2geo['location'][
                'latitude'] if ip2geo else None
        except KeyError:
            out['latitude'] = None

        try:
            out['longitude'] = ip2geo['location'][
                'longitude'] if ip2geo else None
        except KeyError:
            out['longitude'] = None

        if ip2geo:
            traits = ip2geo['traits']
            for k, v in traits.iteritems():
                key = 'trait_%s' % (k)
                out[key] = v

        out.update(meta)

        IPStore = apps.get_model('warehouse', 'IPStore')

        try:
            store = IPStore.objects.get(ip=out['ip'])
        except IPStore.DoesNotExist:
            store = None

        out['nearest_address'] = store.nearest_address if store else None
        out['postal_code'] = store.long_postal_code if store else None

        return out

    @property
    def hydrate_meta(self):
        return self._hydrate_meta()

    @staticmethod
    def get_census_data(q):
        """
        Gets the census data against a given lookup

        Args:
            q (text): query string for text

        Returns:
            json: json for geo
        """
        import requests, json
        from django.apps import apps
        from django.conf import settings

        params = {'q': q, 'sumlevs': None, 'start': None}
        # Geography = apps.get_model('census', 'geography')
        r = requests.get(settings.CENSUS_GEOID_LOOKUP, params=params)

        if r.status_code == 200:
            geoid = json.loads(r.text)['results'][0]['full_geoid']
            from plugins.census.profile import geo_profile
            census_data = geo_profile(geoid)
            return census_data

    def append_census_data(self, q):
        d = self.get_census_data(q)
        self.meta.update({'census': d})
        self.save()
