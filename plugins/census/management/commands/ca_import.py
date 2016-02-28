from django.conf import settings
from django.db import connections
from django.db.utils import IntegrityError, DataError
from django.core.management.base import BaseCommand, CommandError
import csv, os

class Command(BaseCommand):

    def handle(self, **options):
        path_to_file = os.path.join(settings.BASE_DIR, 'docs', 'test.csv')
        cursor = connections['us_census'].cursor()

        with open(path_to_file, 'rb') as csvfile:
            table = 'cacensus2011.geocodes'
            # cursor.execute(
            #     """
            #         DROP TABLE
            #             IF EXISTS {table};
            #         CREATE TABLE cacensus2011.geocodes (
            #             id SERIAL PRIMARY KEY,
            #             geocode BIGINT NOT NULL UNIQUE,
            #             province TEXT NOT NULL,
            #             city TEXT NOT NULL
            #         );

            #     """.format(table=table)
            #     )
            reader = csv.reader(csvfile)
            header = reader.next()
            for row in reader:
                query = """
                    SELECT * FROM {table} WHERE geocode='{geocode}';
                """.format(table=table, geocode=row[0])
                result = cursor.execute(query).fetchall()
                print result

                # query = """
                #     INSERT INTO
                #         {table} (geocode, province, city)
                #     SELECT
                #         '{geocode}', '{province}', '{city}'
                #     """.format(
                #             table = 'cacensus2011.geocodes',
                #             geocode=row[0],
                #             province=row[1],
                #             city=row[2]
                #         )
                # try:
                #     cursor.execute(query)
                # except IntegrityError as e:
                #     print e
                # except DataError as e:
                #     print e
