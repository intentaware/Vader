from django.db import models

from django_extensions.db.fields import *
from django_pgjson.fields import JsonField

from apps.common.models import *
from apps.finances.mixins import Stripe


class Company(TimeStamped, SluggedFromName, Stripe):
    is_active = models.BooleanField(default=False)

    is_advertiser = models.BooleanField(default=False)
    is_publisher = models.BooleanField(default=False)
    """
    TODO:
        we need a better udnerstanding of our business case here. I don't think
        boolena fields is the right strategy here.
    """

    publisher_key = ShortUUIDField(blank=True, null=True)

    advertiser_rate = models.DecimalField(default=0.25, max_digits=4, decimal_places=4)
    publisher_rate = models.DecimalField(default=0.05, max_digits=4, decimal_places=4)

    # stripe
    payment_data = JsonField(blank=True, null=True, default={})

    users = models.ManyToManyField('users.User', through='companies.CompanyUser')
    circles = models.ManyToManyField('metas.Circle', through='metas.PublisherCircle')

    class Meta:
        verbose_name_plural = "companies"

    def __unicode__(self):
        return self.name

    def get_target_campaigns(self, request, campaign_id=None):
        from apps.campaigns.models import Coupon
        if not campaign_id:
            return Coupon.objects.active().exclude(
                    campaign__image=None
                ).order_by('?')[:1]
        else:
            return Coupon.objects.filter(
                    campaign_id=campaign_id,
                    redeemed_on__isnull=True,
                ).order_by('?')[:1]

    @property
    def stripe_customer_id(self):
        """
        sets or gets the stripe customer id in stripe database
        """
        stripe_customer_id = self.payment_data.get('stripe_customer_id', None)
        if not stripe_customer_id:
            customer = self.set_stripe_customer()
            stripe_customer_id = customer.id
        return stripe_customer_id

    @property
    def stripe_customer(self):
        """
        gets the stripe customer json object and python dictionary with all
        the right methods
        """
        customer_id = self.payment_data.get('stripe_customer_id', None)
        if not customer_id:
            customer = self.set_stripe_customer()
        else:
            try:
                customer = self._stripe.Customer.retrieve(self.stripe_customer_id)
            #except self._stripe.error.AuthenticationError as ce:
            except:
                customer = self.set_stripe_customer()
        return customer

    def set_stripe_customer(self):
        owner = self.memberships.filter(is_owner=True)[0].user
        response = self._stripe.Customer.create(
                email=owner.email,
                description=self.name
            )
        self.payment_data['stripe_customer_id'] = response.id
        self.save()
        return response


class CompanyGroup(TimeStamped):
    name = models.CharField(max_length=128)
    company = models.ForeignKey('companies.Company', related_name='groups')
    permissions = JsonField(default=[])

    def __unicode__(self):
        return '%s: %s' %(self.company.name, self.name)


class CompanyUser(TimeStamped):
    user = models.ForeignKey('users.User', related_name='memberships')
    group = models.ForeignKey('companies.CompanyGroup', related_name='memberships')
    company = models.ForeignKey('companies.Company', related_name='memberships')

    # override default group permissions?
    is_owner = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    # default membership for the views
    is_default = models.BooleanField(default=False)

    # check whether the membership is active or not
    is_active = models.BooleanField(default=True)

    # phone number
    phone = models.CharField(max_length=32, blank=True, null=True)

    class Meta:
        unique_together = ('user', 'group', 'company')

    def __unicode__(self):
        return '%s: %s' %(self.company.name, self.user)

    def set_default(self):
        """
        sets the default membership out of all memberships for the current
        user.
        """
        if not self.is_active:
            self.user.memberships.all().update(is_active=False)
            self.is_active = True
            self.save()
