from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework.decorators import detail_route, list_route

from apps.companies.models import Company


class BaseModelViewSet(ModelViewSet):
    permission_classes = (IsAuthenticated, )
    prefetch_args = []

    def get_queryset(self):
        company = self.request.user.memberships.get(is_default=True).company
        return self.model.objects.prefetch_related(*self.prefetch_args).filter(
            company=company
        )


class ReporterViewSet(BaseModelViewSet):

    def _filter(self, pk):
        return {'{name}_id'.format(name=self.model._meta.model_name): pk}

    @detail_route(methods=['get'], url_path='reports/useragents')
    def useragents(self, request, pk=None):
        queryset = self.reporter_model.reporter.filter(
            **self._filter(pk)).bracket_months(3).useragents()

        return Response(queryset, status=200)

    @detail_route(methods=['get'], url_path='reports/history')
    def history(self, request, pk=None):
        queryset = self.reporter_model.reporter.filter(
            **self._filter(pk)).bracket_months(3).frequency_daily()

        return Response(queryset, status=200)

    @detail_route(methods=['get'], url_path='reports/datatable')
    def datatable(self, request, pk):
        period = request.query_params.get('period', 1)
        period = int(period)
        queryset = self.reporter_model.reporter.filter(
            **self._filter(pk)).bracket_months(period).flatten()
        return Response(queryset, status=200)

    @detail_route(methods=['get'], url_path='reports/csv')
    def csv(self, request, pk):
        from apps.common.utils.reporter.csvs import UnicodeDictWriter
        from django.http import HttpResponse

        period = request.query_params.get('period', 1)
        period = int(period)

        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="report.csv"'

        queryset = self.reporter_model.reporter.filter(
            **self._filter(pk)).bracket_months(period).flatten()

        fieldnames = [c['prop'] for c in queryset['columns']]
        writer = UnicodeDictWriter(response, fieldnames=fieldnames, extrasaction='ignore')
        writer.writeheader()
        writer.writerows(queryset['data'])

        return response
