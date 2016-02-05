from django.conf import settings
from geoip2 import database
from geoip2.errors import AddressNotFoundError

from apps.warehouse.models import IPStore

reader = database.Reader(settings.MAXMIND_CITY_DB)

ips = ['99.248.9.54',
       '173.34.75.225',
       '70.54.130.204',
       '67.58.222.87',
       '70.55.50.230',
       '76.71.67.164',
       '70.24.105.229',
       '64.231.136.194',
       '135.0.4.175',
       '173.34.222.226',
       '174.92.74.247',
       '99.231.160.194',
       '184.151.178.201',
       '70.49.149.23',
       '66.49.185.244',
       '70.53.51.197',
       '174.112.43.253',
       '173.34.125.63',
       '64.231.148.82',
       '66.49.190.181',
       '173.32.111.198',
       '70.50.213.134',
       '50.100.149.203',
       '99.230.228.92',
       '184.151.190.55',
       '24.114.51.122',
       '174.118.26.209',
       '73.201.179.235',
       '99.237.95.19',
       '76.71.112.4',
       '76.71.4.24',
       '76.68.126.170',
       '174.115.124.199',
       '99.243.22.198',
       '69.157.66.143',
       '99.226.8.59',
       '70.26.57.62',
       '184.147.122.233',
       '216.165.217.88',
       '99.233.178.15',
       '72.15.61.181', ]

def update_gecode(ip, location):
    from googlemaps import Client
    # from django.conf import settings
    import json

    ip.latitude = location['latitude']
    ip.longitude = location['longitude']

    gmaps = Client(key=settings.GOOGLE_GEOCODE_KEY)
    result = gmaps.reverse_geocode((location['latitude'], location['longitude']
                                    ))
    ip.geocode = json.dumps(result)

    print result

    ip.save()



for ip in ips:
    try:
        ip2geo = reader.city(ip).raw
        location = ip2geo['location']
        store, created = IPStore.objects.get_or_create(ip=ip)
        if created:
            update_gecode(store, location)
    except AddressNotFoundError as e:
        print e
