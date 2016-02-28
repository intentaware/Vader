from django.conf import settings
from django.db import connections
from django.db.utils import IntegrityError
from django.core.management.base import BaseCommand, CommandError
import csv, os

class Command(BaseCommand):

    def handle(self, **options):
        path_to_file = os.path.join(settings.BASE_DIR, 'docs', 'test.csv')
        cursor = connections['us_census'].cursor()

        with open(path_to_file, 'rb') as csvfile:
            reader = csv.reader(csvfile)
            header = reader.next()
            for row in reader:
                #                     WHERE NOT EXISTS
                #        (SELECT 1 FROM {table} WHERE geocode = '{geocode}');
                query = """
                    INSERT INTO
                        {table} (geocode, province, city)
                    SELECT
                        '{geocode}', '{province}', '{city}'
                    """.format(
                            table = 'cacensus2011.geocodes',
                            geocode=row[0],
                            province=row[1],
                            city=row[2]
                        )
                try:
                    cursor.execute(query)
                except IntegrityError as e:
                    print e
