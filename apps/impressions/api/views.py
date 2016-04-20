from rest_framework.response import Response

from apps.api.permissions import PublisherAPIPermission
from apps.impressions.models import Impression
from apps.users.models import User, Visitor

from .mixins import BaseImpression


class GetImpression(BaseImpression):
    permission_classes = (PublisherAPIPermission, )
    template = 'impressions/basic.html'

    def get(self, request, pk=None, b64_string=None):
        if pk:
            try:
                impression = Impression.objects.get(id=pk)
            except Impression.DoesNotExist:
                impression = None
            if b64_string:
                doc = self.decode_base64(b64_string, impression)
                email = doc.get('email', None)
                self.claim_coupon(impression, email) if (
                    email and impression
                ) else None
        else:
            pass
        return Response()

    def claim_coupon(self, impression, email):
        user, created = User.objects.get_or_create(email=email)
        # assign the user to impression object.
        impression.visitor.user = user
        impression.visitor.save()
        impression.save()
        impression.coupon.claim(user)


class GetProfile(BaseImpression):

    def get(self, request):
        return Response({})
