from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from apps.companies.models import Company


class BaseModelViewSet(ModelViewSet):
    permission_classes = (IsAuthenticated,)
    prefetch_args = []

    def get_queryset(self):
        company= self.request.user.memberships.get(is_default=True).company
        return self.model.objects.prefetch_related(*self.prefetch_args).filter(
            company=company)
