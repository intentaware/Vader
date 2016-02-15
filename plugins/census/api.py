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


    def profile(self):
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

        print data
        print result

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

        return doc


