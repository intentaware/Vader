from django.db import models
from django_extensions.db.fields import ShortUUIDField

from apps.common.models import TimeStamped, ToCompany
from .managers import CouponManager, CouponQuerySet, \
        CampaignManager, CampaignQuerySet


class Campaign(TimeStamped, ToCompany):
    """
    inherits created_on, updated_on and company fields
    """
    name = models.CharField(max_length=256, default='')
    description = models.TextField(null=True, blank=True)

    starts_on = models.DateTimeField(null=True, blank=True)
    ends_on = models.DateTimeField(null=True, blank=True)

    # set if it is a coupon ad
    # is_coupon_ad = models.BooleanField(default=False)

    # for ad serving purposes
    # counter = models.BigIntegerField(default=0)
    # serve_limit = models.BigIntegerField(default=100)

    budget = models.DecimalField(default=0.00, max_digits=20, decimal_places=4)
    coupon_value = models.DecimalField(default=1, max_digits=20, decimal_places=4)

    # set the ad to inactive after the limit is served
    is_active = models.BooleanField(default=True)

    # an ad can be part of many industries, we will leverage django-taggit

    # call to action
    # c2a = models.URLField(verbose_name='Call to Action')

    # photologue
    image = models.ForeignKey('photologue.Photo', related_name='campaigns',
        blank=True, null=True)

    objects = CampaignManager.from_queryset(CampaignQuerySet)()

    def __unicode__(self):
        return self.name

    def save(self, *args, **kwargs):
        saved_already = False
        if self.id:
            saved_already = True
        campaign = super(Campaign, self).save(*args, **kwargs)
        if not saved_already:
            # get the amount after taking out adomattic cut
            remaining = self.budget * (1 - self.company.advertiser_rate)
            if self.coupon_value:
                count = int(remaining / self.coupon_value)
                Coupon.objects.generate(self, count)
        return campaign


class CampaignCircle(TimeStamped):
    campaign = models.ForeignKey('campaigns.Campaign')
    circle = models.ForeignKey('companies.Circle')


class Coupon(TimeStamped, ToCompany):
    code = ShortUUIDField()
    campaign = models.ForeignKey(Campaign, related_name='coupons')
    redeemed_on = models.DateTimeField(null=True, blank=True)
    claimed_on = models.DateTimeField(null=True, blank=True)

    value = models.DecimalField(default=1, max_digits=20, decimal_places=4)
    """
    What is the difference between claimed on and redeemed_on?
    claimed_on = when the coupon is assigned a user,
    redeemed_on = when the coupon is verified by advertiser/desk clerk and
    discount is approved
    """
    claimed_by = models.ForeignKey('users.User', blank=True, null=True)

    # overriding custom manager
    objects = CouponManager.from_queryset(CouponQuerySet)()

    def __unicode__(self):
        return 'Campaign: %s, Coupon: %s' %(self.campaign.name, self.code)

    def claim(self, user):
        """
        user claims a coupon
        """
        from django.utils import timezone
        from django.conf import settings
        self.claimed_on = timezone.now()
        self.claimed_by = user
        self.save()
        self.generate_barcode()
        user.send_templated_email('coupons/email.html', {
                'coupon': self,
                'STATIC_URL': settings.STATIC_URL,
                'MEDIA_URL': settings.MEDIA_URL,
            })

    def generate_barcode(self):
        from apps.common.utils.barcodes import BarcodeFromString
        BarcodeFromString(self.code)
