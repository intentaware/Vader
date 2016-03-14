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
    coupon_count = models.PositiveIntegerField(default=0)

    # set the ad to inactive after the limit is served
    is_active = models.BooleanField(default=False)

    # an ad can be part of many industries, we will leverage django-taggit

    # call to action
    # c2a = models.URLField(verbose_name='Call to Action')

    # photologue
    image = models.ForeignKey('photologue.Photo', related_name='campaigns',
        blank=True, null=True)

    # finances
    invoice = models.ForeignKey('finances.Invoice', related_name='campaigns',
        blank=True, null=True)

    circles = models.ManyToManyField('metas.Circle', through='metas.CampaignCircle')

    objects = CampaignManager.from_queryset(CampaignQuerySet)()

    def __unicode__(self):
        return self.name

    def save(self, *args, **kwargs):
        saved_already = False
        if self.id:
            saved_already = True
        campaign = super(Campaign, self).save(*args, **kwargs)
        if not saved_already:
            Coupon.objects.generate(self, self.coupon_count)
            #from .tasks import generate_coupons
            #generate_coupons.delay(self.id, self.coupon_count)
        return campaign

    def set_invoice(self, *args, **kwargs):
        from apps.finances.models import Invoice
        self.invoice = Invoice.objects.create(
                company = self.company,
                *args, **kwargs
            )
        self.save()
        return self.invoice

    # @property
    # def is_paid(self):
    #     if self.invoice:
    #         if self.invoice.is_paid:
    #             return True
    #     return False


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
        sets the coupon to claimed, by setting the 'claimed_on' and
        'claimed_by' properties. Sends the email after with coupon code to the
        end user

        Todo:
            the input parameter 'user' should be replaced with email, also,
            request must be part of this to get the desired customer.

        Params:
            user - must confine to apps.models.User object

        """
        from django.utils import timezone
        from django.conf import settings
        self.claimed_on = timezone.now()
        self.claimed_by = user
        self.save()
        self.generate_barcode()
        subject = "[IntentAware] Your offer code for %s's campaign %s" %(self.company.name, self.campaign.name)
        user.send_templated_email(
            template='emails/coupon-code.html',
            context={
                'coupon': self,
                'STATIC_URL': settings.STATIC_URL,
                'MEDIA_URL': settings.MEDIA_URL,
                },
            subject=subject
            )

    def redeem(self):
        from django.utils import timezone as _tz
        """
        now = _tz.now()
        delta = _tz.timedelta(hours=5)
        print now -self.claimed_on
        if (now - self.claimed_on) < delta:
            self.redeemed_on = now
            self.save()
            return self
        else:
            return self
        """
        now = _tz.now()
        self.redeemed_on = now
        self.save()

    def generate_barcode(self):
        """
        Generates the barcode image for the coupon
        """
        from apps.common.utils.barcodes import BarcodeFromString
        BarcodeFromString(self.code)
