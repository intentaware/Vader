import itertools, json, operator

from django.core import serializers
from django.db.models.manager import Manager, QuerySet
from django.utils import timezone as _tz
from dateutil.relativedelta import *


class BaseReportManager(Manager):
    pass


class BaseReportQuerySet(QuerySet):

    @staticmethod
    def date_range(start_date, end_date, increment, period):
        """
        gets the range from start_date to end date where increment can be any
        valid number and period is either hour, day, or year.

        Args:
            start_date (datetime): starting date
            end_date (datetime): ending date
            increment (int): integer
            period (str): valid values are 'years', 'months', 'weeks', 'days', 'hours',
                        'minutes', 'seconds', 'microseconds'

        Returns:
            name (list): an array of valid dates
        """
        result = []
        nxt = start_date
        delta = relativedelta(**{period: increment})
        while nxt <= end_date:
            result.append(nxt)
            nxt += delta
        return result

    @staticmethod
    def json_serialize(queryset):
        """
        Warning! This is a memory intensive operation. The server may break

        Args:
            queryset (obj): django queryset object

        Returns:
            name (dict): dictionary object
        """
        return serializers.serialize('json', queryset)

    def bracket_months(self, months):
        """
        filters the queryset on number of months given

        Args:
            months (int): the number of months to lookup

        Returns:
            name (obj): queryset object
        """
        end = _tz.now()
        start = end + relativedelta(months=-months)
        return self.filter(added_on__gte=start)

    def frequency_daily(self):
        """
        gets the daily frequency of objects in the given queryset

        Returns:
            name (dict): dictionary object with dates as keys and count as value
        """
        queryset = self.order_by('added_on')

        start = queryset.first().added_on
        end = queryset.last().added_on
        date_range = self.date_range(start, end, 1, 'days')
        doc = dict()

        for dt in date_range:
            doc[dt.date().isoformat()] = queryset.filter(
                added_on__date=dt.date()
            ).count()

        return doc

    def frequency_on_meta_key(self, key):
        queryset = self.filter(meta__has_key=key).values_list(
            'meta',
            flat=True
        )
        queryset = sorted(queryset, key=operator.itemgetter(key))
        doc = list()
        for k, v in itertools.groupby(queryset, key=operator.itemgetter(key)):
            doc.append({k: len(list(v))})
        return doc

    def frequency_on_meta_ip2geo_key(self, key):
        queryset = self.filter(meta__has_key='ip2geo').values_list(
            'meta',
            flat=True
        )
        queryset = map(lambda x: x.get('ip2geo', None), queryset)
        doc = list()

        if key == 'city' or key == 'country':
            # first sorting for groupby
            queryset = sorted(
                queryset,
                key=
                lambda x: x[key]['names']['en'] if x.get(key, None) else None
            )
            for k, v in itertools.groupby(
                queryset,
                key=
                lambda x: x[key]['names']['en'] if x.get(key, None) else None
            ):
                doc.append({k: len(list(v))})

        elif key == 'postal_code':
            queryset = sorted(
                queryset,
                key=
                lambda x: x['postal']['code'] if x.get('postal', None) else None
            )
            for k, v in itertools.groupby(
                queryset,
                key=
                lambda x: x['postal']['code'] if x.get('postal', None) else None
            ):
                doc.append({k: len(list(v))})
        elif key == 'location':
            queryset = sorted(
                queryset,
                key=
                lambda x: x['location'] if x.get('location', None) else None
            )
            for k, v in itertools.groupby(
                queryset,
                key=
                lambda x: x['location'] if x.get('location', None) else None
            ):
                doc.append(
                    {
                        'latitude': k['latitude'],
                        'longitude': k['longitude'],
                        'count': len(list(v))
                    }
                )
        return doc
