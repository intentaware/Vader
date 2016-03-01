from django.conf import settings
from django.db import connections
from django.db.utils import IntegrityError, DataError
from django.core.management.base import BaseCommand, CommandError
import csv, os, codecs

class Command(BaseCommand):

    def handle(self, **options):
        population = os.path.join(settings.BASE_DIR, 'docs', 'test.csv')
        income = os.path.join(settings.BASE_DIR, 'docs', 'income.csv')
        cursor = connections['us_census'].cursor()

        # with codecs.open(population, 'rb', encoding='utf-8', errors='ignore') as csvfile:
        #     print 'importing population data'
        #     table = 'cacensus2011.geocodes'
        #     pop_table = 'cacensus2011.population'
        #     print 'Droping and Creating Tables'
        #     cursor.execute(
        #         """
        #             DROP TABLE
        #                 IF EXISTS {table};
        #             CREATE TABLE {table} (
        #                 id BIGSERIAL PRIMARY KEY UNIQUE,
        #                 geocode BIGINT NOT NULL UNIQUE,
        #                 province TEXT NOT NULL,
        #                 city TEXT NOT NULL
        #             );
        #             DROP TABLE
        #                 IF EXISTS {pop_table};
        #             CREATE TABLE {pop_table} (
        #                 id BIGSERIAL PRIMARY KEY UNIQUE,
        #                 geocode BIGINT NOT NULL,
        #                 topic TEXT NOT NULL,
        #                 characteristics TEXT NOT NULL,
        #                 total DECIMAL NOT NULL,
        #                 male DECIMAL,
        #                 female DECIMAL
        #             )
        #         """.format(table=table, pop_table=pop_table)
        #         )
        #     print 'Drop and Creating Table Done'
        #     print 'Reading CSV file'
        #     reader = csv.reader(csvfile)
        #     header = reader.next()
        #     for row in reader:
        #         # inserting geocodes
        #         query = """
        #             SELECT * FROM {table} WHERE geocode='{geocode}';
        #         """.format(table=table, geocode=row[0])
        #         cursor.execute(query)
        #         result = len(cursor.fetchall())
        #         if result == 0:
        #             print 'Inserting Geocode into Table'
        #             query = """
        #                 INSERT INTO
        #                     {table} (geocode, province, city)
        #                 SELECT
        #                     '{geocode}', '{province}', '{city}'
        #                 """.format(
        #                         table = table,
        #                         geocode=row[0],
        #                         province=row[1],
        #                         city=row[2]
        #                     )
        #             try:
        #                 cursor.execute(query)
        #             except IntegrityError as e:
        #                 print e
        #             except DataError as e:
        #                 print row
        #                 print e

        #         # inserting actual data
        #         print 'Inserting actual data'
        #         query = """
        #             INSERT INTO
        #                 {pop_table} (geocode, topic, characteristics, total, male, female)
        #             SELECT
        #                 '{geocode}', '{topic}', '{characteristics}', '{total}', '{male}', '{female}'
        #         """.format(
        #                 pop_table=pop_table,
        #                 geocode=row[0],
        #                 topic=row[3],
        #                 characteristics=row[4],
        #                 total=row[6] or 0,
        #                 male=row[8] or 0,
        #                 female=row[10] or 0
        #             )
        #         try:
        #             cursor.execute(query)
        #         except DataError as e:
        #             print row
        #             print e

        with codecs.open(income, 'rb', encoding='utf-8', errors='ignore') as csvfile:
            print 'importing income data'
            print 'droping and creating tables'
            income_table = 'cacensus2011.income'
            query = """
                DROP TABLE IF EXISTS {income_table};
                CREATE TABLE {income_table} (
                    id BIGSERIAL PRIMARY KEY UNIQUE,
                    geocode BIGINT NOT NULL,
                    topic TEXT NOT NULL,
                    income DECIMAL NOT NULL
                );
            """.format(income_table=income_table)
            print 'Table Succefully cleaned, Importing CSV now'
            reader = csv.reader(csvfile)
            header = reader.next()
            for row in reader:
                city = row[0]
                query = """
                    SELECT geocode FROM cacensus2011.geocodes WHERE city='{city}';
                """.format(city=city)
                cursor.execute(query)
                result = cursor.fetchall()
                geocode = ''
                if len(result):
                    geocode = result[0][0]
                    print 'geocode found, inserting new row'
                    query = """
                        INSERT INTO
                            {income_table} (geocode, topic, income)
                        SELECT
                            '{geocode}', '{topic}', '{income}';
                    """.format(income_table=income_table,
                            geocode=geocode, topic=row[1], income=row[2])
                    try:
                        cursor.execute(query)
                    except DataError as e:
                        print e


