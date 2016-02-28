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
            pop_table = 'cacensus2011.population'
            cursor.execute(
                """
                    DROP TABLE
                        IF EXISTS {table};
                    CREATE TABLE cacensus2011.geocodes (
                        id SERIAL PRIMARY KEY,
                        geocode BIGINT NOT NULL UNIQUE,
                        province TEXT NOT NULL,
                        city TEXT NOT NULL
                    );
                    DROP TABLE
                        IF EXISTS {pop_table};
                    CREATE TABLE {pop_table} (
                        id SERIAL PRIMARY KEY,
                        geocode BIGINT NOT NULL,
                        topic TEXT NOT NULL,
                        characteristics TEXT NOT NULL,
                        total BIGINT NOT NULL,
                        male BIGINT,
                        female BIGINT
                    )
                """.format(table=table, pop_table=pop_table)
                )
            reader = csv.reader(csvfile)
            header = reader.next()
            for row in reader:
                # inserting geocodes
                query = """
                    SELECT * FROM {table} WHERE geocode='{geocode}';
                """.format(table=table, geocode=row[0])
                cursor.execute(query)
                result = len(cursor.fetchall())
                if result == 0:
                    query = """
                        INSERT INTO
                            {table} (geocode, province, city)
                        SELECT
                            '{geocode}', '{province}', '{city}'
                        """.format(
                                table = table,
                                geocode=row[0],
                                province=row[1],
                                city=row[2]
                            )
                    try:
                        cursor.execute(query)
                    except IntegrityError as e:
                        print e
                    except DataError as e:
                        print e

                # inserting actual data
                query = """
                    INSERT INTO
                        {pop_table} (geocode, topic, characteristics, total, male, female)
                    SELECT
                        '{geocode}', '{topic}', '{characteristics}', '{total}', '{male}', '{female}'
                """.format(
                        pop_table=pop_table,
                        geocode=row[0],
                        topic=row[3],
                        characteristics=row[4],
                        total=row[6],
                        male=row[8],
                        female=row[10]
                    )
                cursor.execute(query)
