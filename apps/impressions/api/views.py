from rest_framework.response import Response

from apps.api.permissions import PublisherAPIPermission
from apps.impressions.models import Impression
from apps.users.models import User, Visitor

from .mixins import BaseImpression


class GetImpression(BaseImpression):
    permission_classes = (PublisherAPIPermission, )
    template = 'impressions/basic.html'

    def get(self, request, pk=None, b64_string=None):
        response = dict()
        campaign = None
        if pk:
            try:
                impression = Impression.objects.get(id=pk)
            except Impression.DoesNotExist:
                impression = None
            if b64_string:
                doc = self.decode_base64(b64_string, impression)

                email = doc.get('email', None)
                response = self.claim_coupon(impression, email) if (
                    email and impression
                ) else None

                campaign = doc.get('campaign', None)
                print campaign
                response = self.get_markup(
                    request, campaign
                ) if campaign else None
        else:
            pass
        print response
        return Response(response)

    def get_markup(self, request, campaign):
        impressions = list()
        visitor, created = Visitor.objects.get_or_create(key=request.visitor)
        if request.user.is_authenticated() and not visitor.user:
            visitor.user = request.user
            visitor.save()
        # TODO:
        #   Why do we need to process meta if we already have campaign id?
        # if not campaign:
        #     meta = self.process_request(request)
        meta = self.process_request(request)
        return {'campaign': campaign, 'meta': meta}

    def claim_coupon(self, impression, email):
        user, created = User.objects.get_or_create(email=email)
        # assign the user to impression object.
        impression.visitor.user = user
        impression.visitor.save()
        impression.save()
        impression.coupon.claim(user)
        return {'data': 'Email Sent Sucesfully'}


class GetProfile(BaseImpression):

    def get(self, request):
        return Response({})
