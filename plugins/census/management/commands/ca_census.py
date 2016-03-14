from django.core.management.base import BaseCommand, CommandError
from plugins.census.canadacensus import CanadaCensus

class Command(BaseCommand):

    def handle(self, **options):
        obj = CanadaCensus()
        obj.GeoCode()
        obj.GeoNom()
        obj.Topic()
        obj.Characteristics()
        obj.GeoProfile()