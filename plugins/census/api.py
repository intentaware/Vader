import operator, math

from collections import OrderedDict
from itertools import groupby, izip

from django.db import connections


PARENT_CHILD_CONTAINMENT = {
    '040': ['050', '060', '101', '140', '150', '160', '500', '610', '620', '950', '960', '970'],
    '050': ['060', '101', '140', '150'],
    '140': ['101', '150'],
    '150': ['101'],
}

SUMLEV_NAMES = {
    "010": {"name": "nation", "plural": ""},
    "020": {"name": "region", "plural": "regions"},
    "030": {"name": "division", "plural": "divisions"},
    "040": {"name": "state", "plural": "states", "tiger_table": "state"},
    "050": {"name": "county", "plural": "counties", "tiger_table": "county"},
    "060": {"name": "county subdivision", "plural": "county subdivisions", "tiger_table": "cousub"},
    "101": {"name": "block", "plural": "blocks", "tiger_table": "tabblock"},
    "140": {"name": "census tract", "plural": "census tracts", "tiger_table": "tract"},
    "150": {"name": "block group", "plural": "block groups", "tiger_table": "bg"},
    "160": {"name": "place", "plural": "places", "tiger_table": "place"},
    "170": {"name": "consolidated city", "plural": "consolidated cities", "tiger_table": "concity"},
    "230": {"name": "Alaska native regional corporation", "plural": "Alaska native regional corporations", "tiger_table": "anrc"},
    "250": {"name": "native area", "plural": "native areas", "tiger_table": "aiannh"},
    "251": {"name": "tribal subdivision", "plural": "tribal subdivisions", "tiger_table": "aits"},
    "256": {"name": "tribal census tract", "plural": "tribal census tracts", "tiger_table": "ttract"},
    "300": {"name": "MSA", "plural": "MSAs", "tiger_table": "metdiv"},
    "310": {"name": "CBSA", "plural": "CBSAs", "tiger_table": "cbsa"},
    "314": {"name": "metropolitan division", "plural": "metropolitan divisions", "tiger_table": "metdiv"},
    "330": {"name": "CSA", "plural": "CSAs", "tiger_table": "csa"},
    "335": {"name": "combined NECTA", "plural": "combined NECTAs", "tiger_table": "cnecta"},
    "350": {"name": "NECTA", "plural": "NECTAs", "tiger_table": "necta"},
    "364": {"name": "NECTA division", "plural": "NECTA divisions", "tiger_table": "nectadiv"},
    "400": {"name": "urban area", "plural": "urban areas", "tiger_table": "uac"},
    "500": {"name": "congressional district", "plural": "congressional districts", "tiger_table": "cd"},
    "610": {"name": "state senate district", "plural": "state senate districts", "tiger_table": "sldu"},
    "620": {"name": "state house district", "plural": "state house districts", "tiger_table": "sldl"},
    "795": {"name": "PUMA", "plural": "PUMAs", "tiger_table": "puma"},
    "850": {"name": "ZCTA3", "plural": "ZCTA3s"},
    "860": {"name": "ZCTA5", "plural": "ZCTA5s", "tiger_table": "zcta5"},
    "950": {"name": "elementary school district", "plural": "elementary school districts", "tiger_table": "elsd"},
    "960": {"name": "secondary school district", "plural": "secondary school districts", "tiger_table": "scsd"},
    "970": {"name": "unified school district", "plural": "unified school districts", "tiger_table": "unsd"},
}

state_fips = {
    "01": "Alabama",
    "02": "Alaska",
    "04": "Arizona",
    "05": "Arkansas",
    "06": "California",
    "08": "Colorado",
    "09": "Connecticut",
    "10": "Delaware",
    "11": "District of Columbia",
    "12": "Florida",
    "13": "Georgia",
    "15": "Hawaii",
    "16": "Idaho",
    "17": "Illinois",
    "18": "Indiana",
    "19": "Iowa",
    "20": "Kansas",
    "21": "Kentucky",
    "22": "Louisiana",
    "23": "Maine",
    "24": "Maryland",
    "25": "Massachusetts",
    "26": "Michigan",
    "27": "Minnesota",
    "28": "Mississippi",
    "29": "Missouri",
    "30": "Montana",
    "31": "Nebraska",
    "32": "Nevada",
    "33": "New Hampshire",
    "34": "New Jersey",
    "35": "New Mexico",
    "36": "New York",
    "37": "North Carolina",
    "38": "North Dakota",
    "39": "Ohio",
    "40": "Oklahoma",
    "41": "Oregon",
    "42": "Pennsylvania",
    "44": "Rhode Island",
    "45": "South Carolina",
    "46": "South Dakota",
    "47": "Tennessee",
    "48": "Texas",
    "49": "Utah",
    "50": "Vermont",
    "51": "Virginia",
    "53": "Washington",
    "54": "West Virginia",
    "55": "Wisconsin",
    "56": "Wyoming",
    "60": "American Samoa",
    "66": "Guam",
    "69": "Commonwealth of the Northern Mariana Islands",
    "72": "Puerto Rico",
    "78": "United States Virgin Islands"
}

def maybe_int(i):
    return int(i) if i else i


def percentify(val):
    return val * 100


def rateify(val):
    return val * 1000

def moe_add(moe_a, moe_b):
    # From http://www.census.gov/acs/www/Downloads/handbooks/ACSGeneralHandbook.pdf
    return math.sqrt(moe_a**2 + moe_b**2)


def moe_ratio(numerator, denominator, numerator_moe, denominator_moe):
    # From http://www.census.gov/acs/www/Downloads/handbooks/ACSGeneralHandbook.pdf
    estimated_ratio = numerator / denominator
    return math.sqrt(numerator_moe**2 + (estimated_ratio**2 * denominator_moe**2)) / denominator


class CensusUS(object):
    ops = {
        '+': operator.add,
        '-': operator.sub,
        '/': operator.div,
        '%': percentify,
        '%%': rateify,
        }
    moe_ops = {
        '+': moe_add,
        '-': moe_add,
        '/': moe_ratio,
        '%': percentify,
        '%%': rateify,
    }


    def __init__(self, geoid=None, acs=None, *args, **kwargs):
        self.cursor = connections['us_census'].cursor()
        self.geoid = geoid
        if acs:
            self.acs = acs
        else:
            self.acs = 'acs2014_5yr'

    def query(self, query_string, **query_args):
        """
        Returns query as a dictionary
        """
        self.cursor.execute(query_string, query_args)
        columns = [col[0] for col in self.cursor.description]
        result = list()
        for row in self.cursor.fetchall():
            result.append(dict(izip(columns, row)))
        return result


    def value_rpn_calc(self, data, rpn_string):
        stack = []
        moe_stack = []
        numerator = None
        numerator_moe = None

        for token in rpn_string.split():
            if token in self.ops:
                b = stack.pop()
                b_moe = moe_stack.pop()

                if token in ('%', '%%'):
                    # Single-argument operators
                    if b is None:
                        c = None
                        c_moe = None
                    else:
                        c = self.ops[token](b)
                        c_moe = self.moe_ops[token](b_moe)
                else:
                    a = stack.pop()
                    a_moe = moe_stack.pop()

                    if a is None or b is None:
                        c = None
                        c_moe = None
                    elif token == '/':
                        # Broken out because MOE ratio needs both MOE and estimates

                        # We're dealing with ratios, not pure division.
                        if a == 0 or b == 0:
                            c = 0
                            c_moe = 0
                        else:
                            c = self.ops[token](a, b)
                            c_moe = moe_ratio(a, b, a_moe, b_moe)
                        numerator = a
                        numerator_moe = round(a_moe, 1)
                    else:
                        c = self.ops[token](a, b)
                        c_moe = self.moe_ops[token](a_moe, b_moe)
            elif token.startswith('b'):
                c = data[token]
                c_moe = data[token + '_moe']
            else:
                c = float(token)
                c_moe = float(token)
            stack.append(c)
            moe_stack.append(c_moe)

        value = stack.pop()
        error = moe_stack.pop()

        if not error:
            error = float(0)

        return (value, error, numerator, numerator_moe)


    def get_comparision_geoids(self):
        geoid = self.geoid
        levels = []


        geoid_parts = geoid.split('US')
        if len(geoid_parts) is not 2:
            raise Exception('Invalid geoid')

        levels.append({
            'relation': 'this',
            'geoid': geoid,
            'coverage': 100.0,
        })

        sumlevel = geoid_parts[0][:3]
        id_part = geoid_parts[1]

        if sumlevel in ('140', '150', '160', '310', '330', '350', '860', '950', '960', '970'):
            result = self.query(
                """
                SELECT * FROM tiger2014.census_geo_containment
                WHERE child_geoid='{geoid}' ORDER BY percent_covered ASC;
                """.format(geoid=geoid)
            )
            for row in result:
                parent_sumlevel_name = SUMLEV_NAMES.get(row['parent_geoid'][:3])['name']

                levels.append({
                    'relation': parent_sumlevel_name,
                    'geoid': row['parent_geoid'],
                    'coverage': row['percent_covered'],
                })

        if sumlevel in ('060', '140', '150'):
            levels.append({
                'relation': 'county',
                'geoid': '05000US' + id_part[:5],
                'coverage': 100.0,
            })

        if sumlevel in ('050', '060', '140', '150', '160', '500', '610', '620', '795', '950', '960', '970'):
            levels.append({
                'relation': 'state',
                'geoid': '04000US' + id_part[:2],
                'coverage': 100.0,
            })

        if sumlevel != '010':
            levels.append({
                'relation': 'nation',
                'geoid': '01000US',
                'coverage': 100.0,
            })

        return levels


    def build_item(self, name, data, parents, rpn_string):
        val = dict([('name', name),
            ('values', dict()),
            ('error', dict()),
            ('numerators', dict()),
            ('numerator_errors', dict())])

        for parent in parents:
            label = parent['relation']
            geoid = parent['geoid']
            data_for_geoid = data.get(geoid) if data else {}

            value = None
            error = None
            numerator = None
            numerator_moe = None

            if data_for_geoid:
                (value, error, numerator, numerator_moe) = self.value_rpn_calc(data_for_geoid, rpn_string)

            # provide 2 decimals of precision, let client decide how much to use
            if value is not None:
                value = round(value, 2)
                error = round(error, 2)

            if numerator is not None:
                numerator = round(numerator, 2)
                numerator_moe = round(numerator_moe, 2)

            val['values'][label] = value
            val['error'][label] = error
            val['numerators'][label] = numerator
            val['numerator_errors'][label] = numerator_moe

        return val

    def convert_geography_data(self, row):
        return dict(full_name=row['display_name'],
                    short_name=row['simple_name'],
                    sumlevel=row['sumlevel'],
                    land_area=row['aland'],
                    full_geoid=row['full_geoid'])


    def get_data(self, table_ids, geoids):
        if type(geoids) != list:
            geoids = [geoids]

        if type(table_ids) != list:
            table_ids = [table_ids]

        from_stmt = """
            {acs}.{table_id}_moe""".format(
                acs=self.acs, table_id=table_ids[0])

        if len(table_ids) > 1:
            from_stmt += ' '
            from_stmt += ' '.join(
                ["""JOIN {acs}.{table_id}_moe USING (geoid)""".format(
                acs=self.acs, table_id=table_id) for table_id in table_ids[1:]])

        sql = """
            SELECT * FROM {from_stmt} WHERE geoid IN {geoids};
            """.format(from_stmt=from_stmt, geoids=tuple(geoids))

        return self.query(sql)

    def map_rows_to_geoid(self, result):
        data = dict()

        for r in result:
            data[r['geoid']] = r

        return data


    def get_profile(self):
        item_levels = self.get_comparision_geoids()
        comparison_geoids = [str(level['geoid']) for level in item_levels]

        doc = dict([
            ('geography', dict()),
            ('demographics', dict()),
            ('economics', dict()),
            ('families', dict()),
            ('housing', dict()),
            ('social', dict())
        ])

        data = self.map_rows_to_geoid(self.get_data('B01001', comparison_geoids))

        lookup_data = dict()

        sql = """
            SELECT DISTINCT full_geoid,sumlevel,display_name,simple_name,aland
                FROM tiger2014.census_name_lookup
                WHERE full_geoid IN {geoids};
            """.format(geoids=tuple(comparison_geoids))

        result = self.query(sql)

        doc['geography']['parents'] = dict()

        for row in result:
            lookup_data[row['full_geoid']] = row

        for item_level in item_levels:
            name = item_level['relation']
            the_geoid = item_level['geoid']
            if name == 'this':
                doc['geography'][name] = self.convert_geography_data(lookup_data[the_geoid])
                doc['geography'][name]['total_population'] = maybe_int(data[the_geoid]['b01001001'])
            else:
                doc['geography']['parents'][name] = self.convert_geography_data(lookup_data[the_geoid])
                doc['geography']['parents'][name]['total_population'] = maybe_int(data[the_geoid]['b01001001'])

        age = dict()
        doc['demographics']['age'] = age
        age_cats = dict()

        age['categories'] = age_cats

        age_cats['percent_under_18'] = self.build_item('Under 18', data, item_levels,
            'b01001003 b01001004 + b01001005 + b01001006 + b01001027 + b01001028 + b01001029 + b01001030 + b01001001 / %')

        age_cats['percent_18_to_64'] = self.build_item('18 to 64', data, item_levels,
            'b01001007 b01001008 + b01001009 + b01001010 + b01001011 + b01001012 + b01001013 + b01001014 + b01001015 + b01001016 + b01001017 + b01001018 + b01001019 + b01001031 + b01001032 + b01001033 + b01001034 + b01001035 + b01001036 + b01001037 + b01001038 + b01001039 + b01001040 + b01001041 + b01001042 + b01001043 + b01001001 / %')
        age_cats['percent_over_65'] = self.build_item('65 and over', data, item_levels,
            'b01001020 b01001021 + b01001022 + b01001023 + b01001024 + b01001025 + b01001044 + b01001045 + b01001046 + b01001047 + b01001048 + b01001049 + b01001001 / %')

        pop_dict = dict()
        age['decades'] = pop_dict
        population_by_age_total = dict()
        population_by_age_male = dict()
        population_by_age_female = dict()
        pop_dict['total'] = population_by_age_total
        pop_dict['male'] = population_by_age_male
        pop_dict['femmale'] = population_by_age_female

        population_by_age_male['0-9'] = self.build_item('0-9', data, item_levels,
            'b01001003 b01001004 + b01001002 / %')
        population_by_age_female['0-9'] = self.build_item('0-9', data, item_levels,
            'b01001027 b01001028 + b01001026 / %')
        population_by_age_total['0-9'] = self.build_item('0-9', data, item_levels,
            'b01001003 b01001004 + b01001027 + b01001028 + b01001001 / %')

        population_by_age_male['10-19'] = self.build_item('10-19', data, item_levels,
            'b01001005 b01001006 + b01001007 + b01001002 / %')
        population_by_age_female['10-19'] = self.build_item('10-19', data, item_levels,
            'b01001029 b01001030 + b01001031 + b01001026 / %')
        population_by_age_total['10-19'] = self.build_item('10-19', data, item_levels,
            'b01001005 b01001006 + b01001007 + b01001029 + b01001030 + b01001031 + b01001001 / %')

        population_by_age_male['20-29'] = self.build_item('20-29', data, item_levels,
            'b01001008 b01001009 + b01001010 + b01001011 + b01001002 / %')
        population_by_age_female['20-29'] = self.build_item('20-29', data, item_levels,
            'b01001032 b01001033 + b01001034 + b01001035 + b01001026 / %')
        population_by_age_total['20-29'] = self.build_item('20-29', data, item_levels,
            'b01001008 b01001009 + b01001010 + b01001011 + b01001032 + b01001033 + b01001034 + b01001035 + b01001001 / %')

        population_by_age_male['30-39'] = self.build_item('30-39', data, item_levels,
            'b01001012 b01001013 + b01001002 / %')
        population_by_age_female['30-39'] = self.build_item('30-39', data, item_levels,
            'b01001036 b01001037 + b01001026 / %')
        population_by_age_total['30-39'] = self.build_item('30-39', data, item_levels,
            'b01001012 b01001013 + b01001036 + b01001037 + b01001001 / %')

        population_by_age_male['40-49'] = self.build_item('40-49', data, item_levels,
            'b01001014 b01001015 + b01001002 / %')
        population_by_age_female['40-49'] = self.build_item('40-49', data, item_levels,
            'b01001038 b01001039 + b01001026 / %')
        population_by_age_total['40-49'] = self.build_item('40-49', data, item_levels,
            'b01001014 b01001015 + b01001038 + b01001039 + b01001001 / %')

        population_by_age_male['50-59'] = self.build_item('50-59', data, item_levels,
            'b01001016 b01001017 + b01001002 / %')
        population_by_age_female['50-59'] = self.build_item('50-59', data, item_levels,
            'b01001040 b01001041 + b01001026 / %')
        population_by_age_total['50-59'] = self.build_item('50-59', data, item_levels,
            'b01001016 b01001017 + b01001040 + b01001041 + b01001001 / %')

        population_by_age_male['60-69'] = self.build_item('60-69', data, item_levels,
            'b01001018 b01001019 + b01001020 + b01001021 + b01001002 / %')
        population_by_age_female['60-69'] = self.build_item('60-69', data, item_levels,
            'b01001042 b01001043 + b01001044 + b01001045 + b01001026 / %')
        population_by_age_total['60-69'] = self.build_item('60-69', data, item_levels,
            'b01001018 b01001019 + b01001020 + b01001021 + b01001042 + b01001043 + b01001044 + b01001045 + b01001001 / %')

        population_by_age_male['70-79'] = self.build_item('70-79', data, item_levels,
            'b01001022 b01001023 + b01001002 / %')
        population_by_age_female['70-79'] = self.build_item('70-79', data, item_levels,
            'b01001046 b01001047 + b01001026 / %')
        population_by_age_total['70-79'] = self.build_item('70-79', data, item_levels,
            'b01001022 b01001023 + b01001046 + b01001047 + b01001001 / %')

        population_by_age_male['80+'] = self.build_item('80+', data, item_levels,
            'b01001024 b01001025 + b01001002 / %')
        population_by_age_female['80+'] = self.build_item('80+', data, item_levels,
            'b01001048 b01001049 + b01001026 / %')
        population_by_age_total['80+'] = self.build_item('80+', data, item_levels,
            'b01001024 b01001025 + b01001048 + b01001049 + b01001001 / %')

        sex_dict = dict()
        doc['demographics']['sex'] = sex_dict
        sex_dict['percent_male'] = self.build_item('Male', data, item_levels,
            'b01001002 b01001001 / %')
        sex_dict['percent_female'] = self.build_item('Female', data, item_levels,
            'b01001026 b01001001 / %')

        data = self.map_rows_to_geoid(self.get_data('B01002', comparison_geoids))
        median_age_dict = dict()
        age['median_age'] = median_age_dict
        median_age_dict['total'] = self.build_item('Median age', data, item_levels,
            'b01002001')
        median_age_dict['male'] = self.build_item('Median age male', data, item_levels,
            'b01002002')
        median_age_dict['female'] = self.build_item('Median age female', data, item_levels,
            'b01002003')

        data = self.map_rows_to_geoid(self.get_data('B03002', comparison_geoids))

        race_dict = dict()
        doc['demographics']['race'] = race_dict

        race_dict['percent_white'] = self.build_item('White', data, item_levels,
            'b03002003 b03002001 / %')

        race_dict['percent_black'] = self.build_item('Black', data, item_levels,
            'b03002004 b03002001 / %')

        race_dict['percent_native'] = self.build_item('Native', data, item_levels,
            'b03002005 b03002001 / %')

        race_dict['percent_asian'] = self.build_item('Asian', data, item_levels,
            'b03002006 b03002001 / %')

        race_dict['percent_islander'] = self.build_item('Islander', data, item_levels,
            'b03002007 b03002001 / %')

        race_dict['percent_other'] = self.build_item('Other', data, item_levels,
            'b03002008 b03002001 / %')

        race_dict['percent_two_or_more'] = self.build_item('Two+', data, item_levels,
            'b03002009 b03002001 / %')

        race_dict['percent_hispanic'] = self.build_item('Hispanic', data, item_levels,
        'b03002012 b03002001 / %')

        # Economics: Per-Capita Income
        # single data point
        data = self.map_rows_to_geoid(self.get_data('B19301', comparison_geoids))

        income_dict = dict()
        doc['economics']['income'] = income_dict

        income_dict['per_capita_income_in_the_last_12_months'] = self.build_item('Per capita income', data, item_levels,
            'b19301001')

        # Economics: Median Household Income
        # single data point
        data = self.map_rows_to_geoid(self.get_data('B19013', comparison_geoids))

        income_dict['median_household_income'] = self.build_item('Median household income', data, item_levels,
            'b19013001')

        # Economics: Household Income Distribution
        # multiple data points, suitable for visualization
        data = self.map_rows_to_geoid(self.get_data('B19001', comparison_geoids))

        income_distribution = dict()
        income_dict['household_distribution'] = income_distribution

        income_distribution['under_50'] = self.build_item('Under $50K', data, item_levels,
            'b19001002 b19001003 + b19001004 + b19001005 + b19001006 + b19001007 + b19001008 + b19001009 + b19001010 + b19001001 / %')
        income_distribution['50_to_100'] = self.build_item('$50K - $100K', data, item_levels,
            'b19001011 b19001012 + b19001013 + b19001001 / %')
        income_distribution['100_to_200'] = self.build_item('$100K - $200K', data, item_levels,
            'b19001014 b19001015 + b19001016 + b19001001 / %')
        income_distribution['over_200'] = self.build_item('Over $200K', data, item_levels,
            'b19001017 b19001001 / %')

        # Economics: Poverty Rate
        # provides separate dicts for children and seniors, with multiple data points, suitable for visualization
        data = self.map_rows_to_geoid(self.get_data('B17001', comparison_geoids))

        poverty_dict = dict()
        doc['economics']['poverty'] = poverty_dict

        poverty_dict['percent_below_poverty_line'] = self.build_item('Persons below poverty line', data, item_levels,
            'b17001002 b17001001 / %')

        poverty_children = dict()
        poverty_seniors = dict()
        poverty_dict['children'] = poverty_children
        poverty_dict['seniors'] = poverty_seniors

        poverty_children['below'] = self.build_item('Poverty', data, item_levels,
            'b17001004 b17001005 + b17001006 + b17001007 + b17001008 + b17001009 + b17001018 + b17001019 + b17001020 + b17001021 + b17001022 + b17001023 + b17001004 b17001005 + b17001006 + b17001007 + b17001008 + b17001009 + b17001018 + b17001019 + b17001020 + b17001021 + b17001022 + b17001023 + b17001033 + b17001034 + b17001035 + b17001036 + b17001037 + b17001038 + b17001047 + b17001048 + b17001049 + b17001050 + b17001051 + b17001052 + / %')
        poverty_children['above'] = self.build_item('Non-poverty', data, item_levels,
            'b17001033 b17001034 + b17001035 + b17001036 + b17001037 + b17001038 + b17001047 + b17001048 + b17001049 + b17001050 + b17001051 + b17001052 + b17001004 b17001005 + b17001006 + b17001007 + b17001008 + b17001009 + b17001018 + b17001019 + b17001020 + b17001021 + b17001022 + b17001023 + b17001033 + b17001034 + b17001035 + b17001036 + b17001037 + b17001038 + b17001047 + b17001048 + b17001049 + b17001050 + b17001051 + b17001052 + / %')

        poverty_seniors['below'] = self.build_item('Poverty', data, item_levels,
            'b17001015 b17001016 + b17001029 + b17001030 + b17001015 b17001016 + b17001029 + b17001030 + b17001044 + b17001045 + b17001058 + b17001059 + / %')
        poverty_seniors['above'] = self.build_item('Non-poverty', data, item_levels,
            'b17001044 b17001045 + b17001058 + b17001059 + b17001015 b17001016 + b17001029 + b17001030 + b17001044 + b17001045 + b17001058 + b17001059 + / %')

        # Economics: Mean Travel Time to Work, Means of Transportation to Work
        # uses two different tables for calculation, so make sure they draw from same ACS release
        data = self.map_rows_to_geoid(self.get_data(['B08006', 'B08013'], comparison_geoids))

        employment_dict = dict()
        doc['economics']['employment'] = employment_dict

        employment_dict['mean_travel_time'] = self.build_item('Mean travel time to work', data, item_levels,
            'b08013001 b08006001 b08006017 - /')

        data = self.map_rows_to_geoid(self.get_data('B08006', comparison_geoids))

        transportation_dict = dict()
        employment_dict['transportation_distribution'] = transportation_dict

        transportation_dict['drove_alone'] = self.build_item('Drove alone', data, item_levels,
            'b08006003 b08006001 / %')
        transportation_dict['carpooled'] = self.build_item('Carpooled', data, item_levels,
            'b08006004 b08006001 / %')
        transportation_dict['public_transit'] = self.build_item('Public transit', data, item_levels,
            'b08006008 b08006001 / %')
        transportation_dict['bicycle'] = self.build_item('Bicycle', data, item_levels,
            'b08006014 b08006001 / %')
        transportation_dict['walked'] = self.build_item('Walked', data, item_levels,
            'b08006015 b08006001 / %')
        transportation_dict['other'] = self.build_item('Other', data, item_levels,
            'b08006016 b08006001 / %')
        transportation_dict['worked_at_home'] = self.build_item('Worked at home', data, item_levels,
            'b08006017 b08006001 / %')

        # Families: Marital Status by Sex
        data = self.map_rows_to_geoid(self.get_data('B12001', comparison_geoids))

        marital_status = dict()
        doc['families']['marital_status'] = marital_status

        marital_status['married'] = self.build_item('Married', data, item_levels,
            'b12001004 b12001013 + b12001001 / %')
        marital_status['single'] = self.build_item('Single', data, item_levels,
            'b12001003 b12001009 + b12001010 + b12001012 + b12001018 + b12001019 + b12001001 / %')

        marital_status_grouped = dict()
        doc['families']['marital_status_grouped'] = marital_status_grouped

        # repeating data temporarily to develop grouped column chart format
        marital_status_grouped['never_married'] = dict()
        marital_status_grouped['never_married']['metadata'] = {
            'universe': 'Population 15 years and over',
            'table_id': 'b12001',
            'name': 'Never married'
        }
        marital_status_grouped['never_married']['male'] = self.build_item('Male', data, item_levels,
            'b12001003 b12001002 / %')
        marital_status_grouped['never_married']['female'] = self.build_item('Female', data, item_levels,
            'b12001012 b12001011 / %')

        marital_status_grouped['married'] = dict()
        marital_status_grouped['married']['metadata'] = {
            'universe': 'Population 15 years and over',
            'table_id': 'b12001',
            'name': 'Now married'
        }
        marital_status_grouped['married']['male'] = self.build_item('Male', data, item_levels,
            'b12001004 b12001002 / %')
        marital_status_grouped['married']['female'] = self.build_item('Female', data, item_levels,
            'b12001013 b12001011 / %')

        marital_status_grouped['divorced'] = dict()
        marital_status_grouped['divorced']['metadata'] = {
            'universe': 'Population 15 years and over',
            'table_id': 'b12001',
            'name': 'Divorced'
        }
        marital_status_grouped['divorced']['male'] = self.build_item('Male', data, item_levels,
            'b12001010 b12001002 / %')
        marital_status_grouped['divorced']['female'] = self.build_item('Female', data, item_levels,
            'b12001019 b12001011 / %')

        marital_status_grouped['widowed'] = dict()
        marital_status_grouped['widowed']['metadata'] = {
            'universe': 'Population 15 years and over',
            'table_id': 'b12001',
            'name': 'Widowed'
        }
        marital_status_grouped['widowed']['male'] = self.build_item('Male', data, item_levels,
            'b12001009 b12001002 / %')
        marital_status_grouped['widowed']['female'] = self.build_item('Female', data, item_levels,
            'b12001018 b12001011 / %')


        # Families: Family Types with Children
        data = self.map_rows_to_geoid(self.get_data('B09002', comparison_geoids))

        family_types = dict()
        doc['families']['family_types'] = family_types

        children_family_type_dict = dict()
        family_types['children'] = children_family_type_dict

        children_family_type_dict['married_couple'] = self.build_item('Married couple', data, item_levels,
            'b09002002 b09002001 / %')
        children_family_type_dict['male_householder'] = self.build_item('Male householder', data, item_levels,
            'b09002009 b09002001 / %')
        children_family_type_dict['female_householder'] = self.build_item('Female householder', data, item_levels,
            'b09002015 b09002001 / %')

        # Families: Birth Rate by Women's Age
        data = self.map_rows_to_geoid(self.get_data('B13016', comparison_geoids))

        fertility = dict()
        doc['families']['fertility'] = fertility

        fertility['total'] = self.build_item('Women 15-50 who gave birth during past year', data, item_levels,
            'b13016002 b13016001 / %')

        fertility_by_age_dict = dict()
        fertility['by_age'] = fertility_by_age_dict

        fertility_by_age_dict['15_to_19'] = self.build_item('15-19', data, item_levels,
            'b13016003 b13016003 b13016011 + / %')
        fertility_by_age_dict['20_to_24'] = self.build_item('20-24', data, item_levels,
            'b13016004 b13016004 b13016012 + / %')
        fertility_by_age_dict['25_to_29'] = self.build_item('25-29', data, item_levels,
            'b13016005 b13016005 b13016013 + / %')
        fertility_by_age_dict['30_to_34'] = self.build_item('30-35', data, item_levels,
            'b13016006 b13016006 b13016014 + / %')
        fertility_by_age_dict['35_to_39'] = self.build_item('35-39', data, item_levels,
            'b13016007 b13016007 b13016015 + / %')
        fertility_by_age_dict['40_to_44'] = self.build_item('40-44', data, item_levels,
            'b13016008 b13016008 b13016016 + / %')
        fertility_by_age_dict['45_to_50'] = self.build_item('45-50', data, item_levels,
            'b13016009 b13016009 b13016017 + / %')

        # Families: Number of Households, Persons per Household, Household type distribution
        data = self.map_rows_to_geoid(self.get_data(['B11001', 'B11002'], comparison_geoids))

        households_dict = dict()
        doc['families']['households'] = households_dict

        households_dict['number_of_households'] = self.build_item('Number of households', data, item_levels,
            'b11001001')

        households_dict['persons_per_household'] = self.build_item('Persons per household', data, item_levels,
            'b11002001 b11001001 /')

        households_distribution_dict = dict()
        households_dict['distribution'] = households_distribution_dict

        households_distribution_dict['married_couples'] = self.build_item('Married couples', data, item_levels,
            'b11002003 b11002001 / %')

        households_distribution_dict['male_householder'] = self.build_item('Male householder', data, item_levels,
            'b11002006 b11002001 / %')

        households_distribution_dict['female_householder'] = self.build_item('Female householder', data, item_levels,
            'b11002009 b11002001 / %')

        households_distribution_dict['nonfamily'] = self.build_item('Non-family', data, item_levels,
            'b11002012 b11002001 / %')


        # Housing: Number of Housing Units, Occupancy Distribution, Vacancy Distribution
        data = self.map_rows_to_geoid(self.get_data('B25002', comparison_geoids))

        units_dict = dict()
        doc['housing']['units'] = units_dict

        units_dict['number'] = self.build_item('Number of housing units', data, item_levels,
            'b25002001')

        occupancy_distribution_dict = dict()
        units_dict['occupancy_distribution'] = occupancy_distribution_dict

        occupancy_distribution_dict['occupied'] = self.build_item('Occupied', data, item_levels,
            'b25002002 b25002001 / %')
        occupancy_distribution_dict['vacant'] = self.build_item('Vacant', data, item_levels,
            'b25002003 b25002001 / %')

        # Housing: Structure Distribution
        data = self.map_rows_to_geoid(self.get_data('B25024', comparison_geoids))

        structure_distribution_dict = dict()
        units_dict['structure_distribution'] = structure_distribution_dict

        structure_distribution_dict['single_unit'] = self.build_item('Single unit', data, item_levels,
            'b25024002 b25024003 + b25024001 / %')
        structure_distribution_dict['multi_unit'] = self.build_item('Multi-unit', data, item_levels,
            'b25024004 b25024005 + b25024006 + b25024007 + b25024008 + b25024009 + b25024001 / %')
        structure_distribution_dict['mobile_home'] = self.build_item('Mobile home', data, item_levels,
            'b25024010 b25024001 / %')
        structure_distribution_dict['vehicle'] = self.build_item('Boat, RV, van, etc.', data, item_levels,
            'b25024011 b25024001 / %')

        # Housing: Tenure
        data = self.map_rows_to_geoid(self.get_data('B25003', comparison_geoids))

        ownership_dict = dict()
        doc['housing']['ownership'] = ownership_dict

        ownership_distribution_dict = dict()
        ownership_dict['distribution'] = ownership_distribution_dict

        ownership_distribution_dict['owner'] = self.build_item('Owner occupied', data, item_levels,
            'b25003002 b25003001 / %')
        ownership_distribution_dict['renter'] = self.build_item('Renter occupied', data, item_levels,
            'b25003003 b25003001 / %')

        data = self.map_rows_to_geoid(self.get_data('B25026', comparison_geoids))

        length_of_tenure_dict = dict()
        doc['housing']['length_of_tenure'] = length_of_tenure_dict

        length_of_tenure_dict['before_1970'] = self.build_item('Before 1970', data, item_levels,
            'b25026008 b25026015 + b25026001 / %')
        length_of_tenure_dict['1970s'] = self.build_item('1970s', data, item_levels,
            'b25026007 b25026014 + b25026001 / %')
        length_of_tenure_dict['1980s'] = self.build_item('1980s', data, item_levels,
            'b25026006 b25026013 + b25026001 / %')
        length_of_tenure_dict['1990s'] = self.build_item('1990s', data, item_levels,
            'b25026005 b25026012 + b25026001 / %')
        length_of_tenure_dict['2000_to_2004'] = self.build_item('2000-2004', data, item_levels,
            'b25026004 b25026011 + b25026001 / %')
        length_of_tenure_dict['since_2005'] = self.build_item('Since 2005', data, item_levels,
            'b25026003 b25026010 + b25026001 / %')

        # Housing: Mobility
        data = self.map_rows_to_geoid(self.get_data('B07003', comparison_geoids))

        migration_dict = dict()
        doc['housing']['migration'] = migration_dict

        migration_dict['moved_since_previous_year'] = self.build_item('Moved since previous year', data, item_levels,
            'b07003007 b07003010 + b07003013 + b07003016 + b07003001 / %')

        migration_distribution_dict = dict()
        doc['housing']['migration_distribution'] = migration_distribution_dict

        migration_distribution_dict['same_house_year_ago'] = self.build_item('Same house year ago', data, item_levels,
            'b07003004 b07003001 / %')
        migration_distribution_dict['moved_same_county'] = self.build_item('From same county', data, item_levels,
            'b07003007 b07003001 / %')
        migration_distribution_dict['moved_different_county'] = self.build_item('From different county', data, item_levels,
            'b07003010 b07003001 / %')
        migration_distribution_dict['moved_different_state'] = self.build_item('From different state', data, item_levels,
            'b07003013 b07003001 / %')
        migration_distribution_dict['moved_from_abroad'] = self.build_item('From abroad', data, item_levels,
            'b07003016 b07003001 / %')

        # Housing: Median Value and Distribution of Values
        data = self.map_rows_to_geoid(self.get_data('B25077', comparison_geoids))

        ownership_dict['median_value'] = self.build_item('Median value of owner-occupied housing units', data, item_levels,
            'b25077001')

        data = self.map_rows_to_geoid(self.get_data('B25075', comparison_geoids))

        value_distribution = dict()
        ownership_dict['value_distribution'] = value_distribution

        ownership_dict['total_value'] = self.build_item('Total value of owner-occupied housing units', data, item_levels,
            'b25075001')

        value_distribution['under_100'] = self.build_item('Under $100K', data, item_levels,
            'b25075002 b25075003 + b25075004 + b25075005 + b25075006 + b25075007 + b25075008 + b25075009 + b25075010 + b25075011 + b25075012 + b25075013 + b25075014 + b25075001 / %')
        value_distribution['100_to_200'] = self.build_item('$100K - $200K', data, item_levels,
            'b25075015 b25075016 + b25075017 + b25075018 + b25075001 / %')
        value_distribution['200_to_300'] = self.build_item('$200K - $300K', data, item_levels,
            'b25075019 b25075020 + b25075001 / %')
        value_distribution['300_to_400'] = self.build_item('$300K - $400K', data, item_levels,
            'b25075021 b25075001 / %')
        value_distribution['400_to_500'] = self.build_item('$400K - $500K', data, item_levels,
            'b25075022 b25075001 / %')
        value_distribution['500_to_1000000'] = self.build_item('$500K - $1M', data, item_levels,
            'b25075023 b25075024 + b25075001 / %')
        value_distribution['over_1000000'] = self.build_item('Over $1M', data, item_levels,
            'b25075025 b25075001 / %')


        # Social: Educational Attainment
        # Two aggregated data points for "high school and higher," "college degree and higher"
        # and distribution dict for chart
        data = self.map_rows_to_geoid(self.get_data('B15002', comparison_geoids))

        attainment_dict = dict()
        doc['social']['education'] = attainment_dict

        attainment_dict['percent_high_school_grad_or_higher'] = self.build_item('High school grad or higher', data, item_levels,
            'b15002011 b15002012 + b15002013 + b15002014 + b15002015 + b15002016 + b15002017 + b15002018 + b15002028 + b15002029 + b15002030 + b15002031 + b15002032 + b15002033 + b15002034 + b15002035 + b15002001 / %')

        attainment_dict['percent_bachelor_degree_or_higher'] = self.build_item('Bachelor\'s degree or higher', data, item_levels,
            'b15002015 b15002016 + b15002017 + b15002018 + b15002032 + b15002033 + b15002034 + b15002035 + b15002001 / %')

        attainment_distribution_dict = dict()
        doc['social']['education']['distribution'] = attainment_distribution_dict

        attainment_distribution_dict['non_high_school_grad'] = self.build_item('No degree', data, item_levels,
            'b15002003 b15002004 + b15002005 + b15002006 + b15002007 + b15002008 + b15002009 + b15002010 + b15002020 + b15002021 + b15002022 + b15002023 + b15002024 + b15002025 + b15002026 + b15002027 + b15002001 / %')

        attainment_distribution_dict['high_school_grad'] = self.build_item('High school', data, item_levels,
            'b15002011 b15002028 + b15002001 / %')

        attainment_distribution_dict['some_college'] = self.build_item('Some college', data, item_levels,
            'b15002012 b15002013 + b15002014 + b15002029 + b15002030 + b15002031 + b15002001 / %')

        attainment_distribution_dict['bachelor_degree'] = self.build_item('Bachelor\'s', data, item_levels,
            'b15002015 b15002032 + b15002001 / %')

        attainment_distribution_dict['post_grad_degree'] = self.build_item('Post-grad', data, item_levels,
            'b15002016 b15002017 + b15002018 + b15002033 + b15002034 + b15002035 + b15002001 / %')

        # Social: Place of Birth
        data = self.map_rows_to_geoid(self.get_data('B05002', comparison_geoids))

        foreign_dict = dict()
        doc['social']['place_of_birth'] = foreign_dict

        foreign_dict['percent_foreign_born'] = self.build_item('Foreign-born population', data, item_levels,
            'b05002013 b05002001 / %')

        data = self.map_rows_to_geoid(self.get_data('B05006', comparison_geoids))

        place_of_birth_dict = dict()
        foreign_dict['distribution'] = place_of_birth_dict

        place_of_birth_dict['europe'] = self.build_item('Europe', data, item_levels,
            'b05006002 b05006001 / %')
        place_of_birth_dict['asia'] = self.build_item('Asia', data, item_levels,
            'b05006047 b05006001 / %')
        place_of_birth_dict['africa'] = self.build_item('Africa', data, item_levels,
            'b05006091 b05006001 / %')
        place_of_birth_dict['oceania'] = self.build_item('Oceania', data, item_levels,
            'b05006116 b05006001 / %')
        place_of_birth_dict['latin_america'] = self.build_item('Latin America', data, item_levels,
            'b05006123 b05006001 / %')
        place_of_birth_dict['north_america'] = self.build_item('North America', data, item_levels,
            'b05006159 b05006001 / %')

        # Social: Percentage of Non-English Spoken at Home, Language Spoken at Home for Children, Adults
        data = self.map_rows_to_geoid(self.get_data('B16001', comparison_geoids))

        language_dict = dict()
        doc['social']['language'] = language_dict

        language_dict['percent_non_english_at_home'] = self.build_item('Persons with language other than English spoken at home', data, item_levels,
            'b16001001 b16001002 - b16001001 / %')


        data = self.map_rows_to_geoid(self.get_data('B16007', comparison_geoids))

        language_children = dict()
        language_adults = dict()
        language_dict['children'] = language_children
        language_dict['adults'] = language_adults

        language_children['english'] = self.build_item('English only', data, item_levels,
            'b16007003 b16007002 / %')
        language_adults['english'] = self.build_item('English only', data, item_levels,
            'b16007009 b16007015 + b16007008 b16007014 + / %')

        language_children['spanish'] = self.build_item('Spanish', data, item_levels,
            'b16007004 b16007002 / %')
        language_adults['spanish'] = self.build_item('Spanish', data, item_levels,
            'b16007010 b16007016 + b16007008 b16007014 + / %')

        language_children['indoeuropean'] = self.build_item('Indo-European', data, item_levels,
            'b16007005 b16007002 / %')
        language_adults['indoeuropean'] = self.build_item('Indo-European', data, item_levels,
            'b16007011 b16007017 + b16007008 b16007014 + / %')

        language_children['asian_islander'] = self.build_item('Asian/Islander', data, item_levels,
            'b16007006 b16007002 / %')
        language_adults['asian_islander'] = self.build_item('Asian/Islander', data, item_levels,
            'b16007012 b16007018 + b16007008 b16007014 + / %')

        language_children['other'] = self.build_item('Other', data, item_levels,
            'b16007007 b16007002 / %')
        language_adults['other'] = self.build_item('Other', data, item_levels,
            'b16007013 b16007019 + b16007008 b16007014 + / %')


        # Social: Number of Veterans, Wartime Service, Sex of Veterans
        data = self.map_rows_to_geoid(self.get_data('B21002', comparison_geoids))

        veterans_dict = dict()
        doc['social']['veterans'] = veterans_dict

        veterans_service_dict = dict()
        veterans_dict['wartime_service'] = veterans_service_dict

        veterans_service_dict['wwii'] = self.build_item('WWII', data, item_levels,
            'b21002009 b21002011 + b21002012 +')
        veterans_service_dict['korea'] = self.build_item('Korea', data, item_levels,
            'b21002008 b21002009 + b21002010 + b21002011 +')
        veterans_service_dict['vietnam'] = self.build_item('Vietnam', data, item_levels,
            'b21002004 b21002006 + b21002007 + b21002008 + b21002009 +')
        veterans_service_dict['gulf_1990s'] = self.build_item('Gulf (1990s)', data, item_levels,
            'b21002003 b21002004 + b21002005 + b21002006 +')
        veterans_service_dict['gulf_2001'] = self.build_item('Gulf (2001-)', data, item_levels,
            'b21002002 b21002003 + b21002004 +')

        data = self.map_rows_to_geoid(self.get_data('B21001', comparison_geoids))

        veterans_sex_dict = dict()
        veterans_dict['sex'] = veterans_sex_dict

        veterans_sex_dict['male'] = self.build_item('Male', data, item_levels,
            'b21001005')
        veterans_sex_dict['female'] = self.build_item('Female', data, item_levels,
            'b21001023')

        veterans_dict['number'] = self.build_item('Total veterans', data, item_levels,
            'b21001002')

        veterans_dict['percentage'] = self.build_item('Population with veteran status', data, item_levels,
            'b21001002 b21001001 / %')

        return doc

    def computed_profile(self):
        doc = dict()
        profile = self.get_profile()

        age = profile['demographics']['age']['median_age']['total']['values']['this']
        doc['age'] = int(age)

        male = profile['demographics']['sex']['percent_male']['values']['this']
        female = profile['demographics']['sex']['percent_female']['values']['this']
        if male > female:
            doc['sex'] = 'Male'
        else:
            doc['sex'] = 'Female'

        transport = dict([
            ('Bicycle', profile['economics']['employment']['transportation_distribution']['bicycle']['values']['this']),
            ('Public Transit', profile['economics']['employment']['transportation_distribution']['public_transit']['values']['this']),
            ('Works At Home', profile['economics']['employment']['transportation_distribution']['worked_at_home']['values']['this']),
            ('Car Pools', profile['economics']['employment']['transportation_distribution']['carpooled']['values']['this']),
            ('Walks', profile['economics']['employment']['transportation_distribution']['walked']['values']['this']),
            ('Drives Alone', profile['economics']['employment']['transportation_distribution']['drove_alone']['values']['this'])
        ])
        doc['transport'] = max(transport.iteritems(), key=operator.itemgetter(1))[0]

        income = profile['economics']['income']['per_capita_income_in_the_last_12_months']['values']['this']
        if income > 49999:
            doc['job'] = 'Blue Collar'
        else:
            doc['job'] = 'White Collar'

        education = dict([
            ('Bechelors', profile['social']['education']['distribution']['bachelor_degree']['values']['this']),
            ('High School Dropout', profile['social']['education']['distribution']['non_high_school_grad']['values']['this']),
            ('Post Graduate', profile['social']['education']['distribution']['post_grad_degree']['values']['this']),
            ('High School', profile['social']['education']['distribution']['high_school_grad']['values']['this']),
            ('Some College', profile['social']['education']['distribution']['some_college']['values']['this']),
        ])

        doc['education'] = max(education.iteritems(), key=operator.itemgetter(1))[0]

        return doc

