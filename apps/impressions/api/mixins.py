import json

from django.conf import settings
from django.template.loader import render_to_string
from django.template import RequestContext

from rest_framework.views import APIView
from rest_framework.response import Response

from ipware.ip import get_real_ip

from geoip2 import database, webservice

from apps.api.permissions import PublisherAPIPermission
from apps.impressions.models import Impression
from apps.users.models import User, Visitor
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
            ip (string): IP v4 address normally in the range xxx.xxx.xxx.xxx where x is a number
            from_db (Boolean, optional): condition to check if we should get the data from maxmind API or locally.

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

    def get_US_census(self, postcode):
        pass

    def get_CA_census(self, postcode, city):
        pass

    def get_census_data(self, country, postcode, city=None):
        """
        Call the respective API to accumulate the cencus data

        Args:
            country (string):   country iso code, for example CA for Canada, US for United States
            postcode (string):  the postal code for the the place for which the census data is required
            city (None, optional): city, as an option for fallback if the  postcode data is not available.

        Returns:
            census (dict): census dictionary object
        """
        census = None
        if country == 'US':
            census = self.get_US_census(postcode)
        if country == 'CA':
            census = self.get_CA_census(postcode, city)
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
        doc = self.parse_request_meta(request, doc)

        if ip2geo:
            country = ip2geo['country']['iso_code']
            city = ip2geo['city']['names']['en']
            postcode = ip2geo['postal']['code']

        else:
            country = city = postcode = None

        doc['census'] = self.get_census_data(country, postcode, city)
