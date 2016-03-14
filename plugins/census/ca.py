from django.db import connections


class CaCensus(object):

    def __init__(self, city, *args, **kwargs):
        self.cursor = connections['us_census'].cursor()
        self.city = city

    def get_geocode(self):
        print self.city
        query = """
            SELECT geocode FROM cacensus2011.geocodes WHERE city='{city}';
        """.format(city=self.city)

        self.cursor.execute(query)
        result = self.cursor.fetchall()

        geocode = None

        if len(result):
            geocode = result[0][0]

        print geocode

        self.geocode = geocode

        return geocode

    def get_population(self):
        geocode = self.get_geocode()
        doc = dict()
        results = None
        if geocode:
            query = """
                SELECT
                    *
                FROM
                    cacensus2011.population
                WHERE
                    geocode='{geocode}';
                """.format(geocode=geocode)
            self.cursor.execute(query)
            results = self.cursor.fetchall()
            if len(results):
                for row in results:
                    if 'population by age' in row[3]:
                        doc['total'] = row[4]
                        doc['male'] = row[5]
                        doc['female'] = row[6]

                    elif 'Median' in row[3]:
                        doc['median_overall'] = row[4]
                        doc['median_male'] = row[5]
                        doc['median_female'] = row[6]

                print doc

        return doc

    def get_income(self):
        if not hasattr(self, 'geocode'):
            geocode = self.get_geocode()
        else:
            geocode = self.geocode

        income = 40000

        doc = dict()

        if geocode:
            query = """
                SELECT * FROM cacensus2011.income WHERE geocode='{geocode}';
                """.format(geocode=geocode)

            self.cursor.execute(query)

            results = self.cursor.fetchall()

        for row in results:
            if 'Average' in row[2]:
                income = row[3]

        return income

    def get_profile(self):
        doc = dict()

        population = self.get_population()
        if len(population):
            if population['male'] > population['female']:
                doc['sex'] = 'Male'
                doc['age'] = int(population['median_male'])
            else:
                doc['sex'] = 'Female'
                doc['age'] = int(population['median_female'])

        income = self.get_income()

        if int(income) > 45000:
            doc['job'] = 'White Collar'
        else:
            doc['job'] = 'Blue Collar'

        return doc
