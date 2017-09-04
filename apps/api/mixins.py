import json

from django.conf import settings
from django.template.loader import render_to_string
from django.template import RequestContext

from rest_framework.views import APIView
from rest_framework.response import Response

from ipware.ip import get_real_ip

from googlemaps import Client
from geoip2 import database, webservice

from apps.warehouse.models import IPStore

from plugins.census.models import Geography
from plugins.census.api import CensusUS
from plugins.census.ca import CaCensus


class BaseImpression(APIView):

    def get_ip_traits(self, ip, from_db=None):
        """
        Gets the data from Maxmind IP Warehouse.
        This generate starts the process

        Args:
            ip (string): IP v4 address normally in the range xxx.xxx.xxx.xxx
                where x is a number and the value of xxx is always less than 256
            from_db (Boolean, optional): condition to check if we should get
                the data from maxmind API or locally.

        Returns:
            doc (dict): dictionary object
        """
        if from_db:
            reader = database.Reader(settings.MAXMIND_CITY_DB)
            ip2geo = reader.city(ip).raw
        else:
            reader = webservice.Client(
                settings.MAXMIND_CLIENTID, settings.MAXMIND_SECRET
            )
            ip2geo = reader.insights(ip).raw
        return ip2geo

    def parse_request_meta(self, request, doc):
        """updates the campaign lookup with request meta

        Args:
            request (obj): the default django request object coming with request
            doc (dict): normal python dictionary object

        Returns:
            doc (dict): updates the dictionary
        """
        for k, v in request.META.iteritems():
            if 'HTTP_' in k:
                k = k.split('HTTP_')[1].lower()
                doc[k] = v
            elif not 'wsgi' in k:
                doc[k.lower()] = v
        return doc

    def get_from_ipstore(self, ip, postcode):
        """
        Gets the census data from IPStore if the postal code exists

        Args:
            ip (string): IP v4 in the format xxx.xxx.xxx.xxx
            postcode (string): Long format postal code

        Returns:
            census (dict): dictionary object containing census data
        """
        census = None

        ipstore, created = IPStore.objects.get_or_create(ip=ip)

        if ipstore.census:
            census = ipstore.census
        else:
            queryset = IPStore.objects.filter(
                geocoded_postal_code=postcode,
                census__isnull=False
            )

            if queryset.count():
                ipstore.census = queryset[0].census
                ipstore.geocoded_postal_code = queryset[0].geocoded_postal_code
                ipstore.save()
                census = queryset[0].census            

        # if created or not ipstore.census:
        #     queryset = IPStore.objects.filter(
        #         geocoded_postal_code=postcode,
        #         census__isnull=False
        #     )

        #     if queryset.count():
        #         ipstore.census = queryset[0].census
        #         ipstore.geocoded_postal_code = queryset[0].geocoded_postal_code
        #         ipstore.save()
        #         census = queryset[0].census
        # else:
        #     census = ipstore.census

        # try:
        #     ipstore = IPStore.objects.get(ip=ip)
        # except:
        #     queryset = IPStore.objects.filter(
        #         geocoded_postal_code=postcode,
        #         census__isnull=False
        #     )
        #     if queryset.count():
        #         ipstore = queryset[0]
        #     else:
        #         ipstore = None

        return census, ipstore

    def get_US_census(self, postcode):
        geoid = Geography.objects.get(
            full_name__contains=postcode
        ).full_geoid.replace('|', '00US')
        return CensusUS(geoid=geoid).computed_profile()

    def get_CA_census(self, postcode, city, location, ip):
        gmaps = Client(key=settings.GOOGLE_GEOCODE_KEY)
        results = gmaps.reverse_geocode(
            (location['latitude'], location['longitude'])
        )

        for r in results[0]['address_components']:
            try:
                types = r['types']
                if types[0] == 'locality' and types[1] == 'political':
                    city = r['long_name']
                    if city == 'Mississauga':
                        city = 'Toronto'

                if types[0] == 'postal_code':
                    postcode = r['long_name']
            except:
                pass

        # first try from IPStore, else lookup census database and update the
        #  ipstore in the process
        census, ipstore = self.get_from_ipstore(ip, postcode)
        
        if not census:
            census = CaCensus(city=city).get_profile()
            ipstore.census = census
            ipstore.geocode = results
            ipstore.geocoded_postal_code=postcode
            ipstore.save()
            # IPStore.objects.create(
            #     ip=ip,
            #     census=census,
            #     geocode=results,
            #     geocoded_postal_code=postcode
            # )
        return census

    def get_census_data(self, country, postcode, city, location, ip):
        """
        Call the respective API to accumulate the cencus data

        Args:
            country (string): country iso code, for example CA for Canada,
                US for United States
            postcode (string): the postal code for the the place for which the
                census data is required
            city (None, optional): city, as an option for fallback if the
                postcode data is not available.
            location (None, optional): dictionary with latitude and longitude
                as keys.
            ip (None, optional): IP v4 Address in the format xxx.xxx.xxx.xxx
                where xxx is always less than 256

        Returns:
            census (dict): census dictionary object
        """
        census = None
        if country == 'US':
            census = self.get_US_census(postcode)
        if country == 'CA':
            census = self.get_CA_census(postcode, city, location, ip)
        return census

    def process_request(self, request):
        """
        Inspects requests, get all the relavant data from different part of our
        data warehouse.

        Args:
            request (obj): django default request object

        Returns:
            doc (dict): dictionary object
        """
        ip = get_real_ip(request) or settings.CENSUS_MOCK_IP
        ip2geo = self.get_ip_traits(ip)

        doc = dict()
        doc['ip2geo'] = ip2geo
        doc['ip'] = ip
        doc = self.parse_request_meta(request, doc)

        if ip2geo:
            country = ip2geo['country']['iso_code']
            city = ip2geo['city']['names']['en']
            postcode = ip2geo['postal']['code']
            location = ip2geo['location']

        else:
            country = city = postcode = None

        doc['census'] = self.get_census_data(
            country, postcode, city, location, ip
        )

        return doc

    def decode_base64(self, encoded_string, model=None):
        """
        decodes the querystring to return parameters

        TODO:
            i am not really sure base64 is the right encoding, because if we are
            sending the data over https, MITM is out of question.

        Args:
            encoded_string (string): base64 encoded string
            model (obj): django model object

        Returns:
            name (obj): django model objects
        """
        from base64 import b64encode, b64decode
        data = json.loads(b64decode(encoded_string))

        doc = dict()
        for key, val in data.iteritems():
            if key == 'meta':
                j = json.loads(val)
                for k, v in j.iteritems():
                    doc[k] = v
            else:
                doc[key] = val
        if model:
            self.update_meta(doc, model)
        return doc

    def update_meta(self, dictionary, model):
        """
        updates model meta data

        Args:
            dictionary (dict): dictionary of items
            model (obj): model who Json field meta is to be updated

        Returns:
            None: returns nothing

        """
        for key, val in dictionary.iteritems():
            """
            the reason we are updating it like this, we want the dictionary to
            update if the key already exists
            """
            model.meta[key] = val
        model.save()
