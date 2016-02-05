from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet


class BaseModelViewSet(ModelViewSet):
    permission_classes = (IsAuthenticated,)
    prefetch_args = []

    def get_queryset(self):
        return self.model.objects.prefetch_related(*self.prefetch_args).filter(
            company=self.request.session.get('company'))
