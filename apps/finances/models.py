import shortuuid
from django.db import models
from django.utils.text import slugify, Truncator
from django.contrib.postgres.fields import JSONField
from django_extensions.db.fields import ShortUUIDField
from apps.common.models import *
from apps.common.utils.money import convert_to_cents
from .mixins import Stripe, CURRENCY_CHOICES


class BasePaymentModel(Stripe, TimeStamped):
    """Basic Payment Model, inherits Stripe model, will be used for multiple


    Attributes:
        amount (Decimal): total amount charged to customer
        attempted_on (Time): time on which the charge was attempted
        attempts (Int): Number of times we tried to charge
        charged_on (Time): If charge was succesful, populate the field with current time
        gateway_response (Json): Response from the server
        is_paid (Bool): if charge was succesful
        service_charges (Decimal): Service charges if any, amount is inclusive of service_charges
        taxes (Decimal): Taxes if any, Note: amount is inclusive of taxes
    """
    amount = models.DecimalField(default=0.00, max_digits=20, decimal_places=4)
    currency = models.CharField(
        max_length=4,
        choices=CURRENCY_CHOICES,
        default='USD'
    )
    attempts = models.IntegerField(default=0)

    #service charges
    service_charges = models.DecimalField(
        default=0.00,
        max_digits=20,
        decimal_places=4
    )
    taxes = models.DecimalField(default=0.0, max_digits=20, decimal_places=4)
    #total_amount = models.DecimalField(default=0.00, max_digits=20, decimal_places=4)

    # extra timestamps
    attempted_on = models.DateTimeField(blank=True, null=True)
    charged_on = models.DateTimeField(blank=True, null=True)

    # json mapped response from stripe
    gateway_response = JSONField(default={})

    is_paid = models.BooleanField(default=False)

    class Meta:
        abstract = True

    @property
    def line_items_total(self):
        return self.amount - self.service_charges - self.taxes


class Invoice(BasePaymentModel):
    stripe_id = models.CharField(
        max_length=256,
        blank=True,
        null=True,
        help_text='id obtained from stripe'
    )
    company = models.ForeignKey('companies.Company', related_name='invoices')


class Module(TimeStamped):
    [CORE, DMP, REPORTING] = range(3)
    SEGMENT_CHOICES = [
        (CORE, 'Core'),
        (DMP, 'Data Management Platform'),
        (REPORTING, 'Reporting'),
    ]

    name = models.CharField(max_length=128, help_text='The name of the module')
    segment = models.IntegerField(
        choices=SEGMENT_CHOICES,
        default=CORE,
        help_text='The segment it is part of'
    )

    def __unicode__(self):
        return self.name


class Plan(TimeStamped, Stripe):
    [UNTIL_EXPIRY, DAY, WEEK, MONTH, YEAR] = range(5)
    INTERVAL_CHOICES = [
        (UNTIL_EXPIRY, 'untill expiry'),
        (DAY, 'day'),
        (WEEK, 'week'),
        (MONTH, 'month'),
        (YEAR, 'year'),
    ]

    amount = models.DecimalField(default=0.00, max_digits=20, decimal_places=2)
    currency = models.CharField(
        max_length=4,
        choices=CURRENCY_CHOICES,
        default='USD'
    )
    name = models.CharField(max_length=128)
    interval = models.IntegerField(
        choices=INTERVAL_CHOICES,
        default=UNTIL_EXPIRY
    )
    modules = models.ManyToManyField(Module, through='finances.PlanModule')
    limit_campaigns = models.IntegerField(
        default=0,
        help_text='0 means unlimited'
    )
    limit_impressions = models.IntegerField(
        default=0,
        help_text='0 means unlimited'
    )

    stripe_id = ShortUUIDField(blank=True, null=True)

    def __unicode__(self):
        return self.name

    def save(self, *args, **kwargs):
        plan = None
        sd = self.stripe_dictionary
        if sd and self.stripe_id:
            try:
                plan = self._stripe.Plan.retrieve(self.stripe_id)
                if not plan.amount == convert_to_cents(self.amount) or not plan.currency == self.currency:
                    self.stripe_id = shortuuid.uuid()
                    self.id = None
                    self.create_stripe_plan()
            except self._stripe.error.InvalidRequestError:
                self.create_stripe_plan()
        return super(Plan, self).save(*args, **kwargs)

    def create_stripe_plan(self, *args, **kwargs):
        self._stripe.Plan.create(**self.stripe_dictionary)

    def features(self):
        from itertools import groupby
        modules = Module.objects.all().values('id', 'name', 'segment')
        plan_modules = self.modules.all().values('id', 'name', 'segment')
        for m in modules:
            if m in plan_modules:
                m['is_included'] = True
            else:
                m['is_included'] = False

        doc = dict()

        for k, v in groupby(modules, lambda x: x['segment']):
            doc[Module.SEGMENT_CHOICES[k][1]] = list(v)

        return doc

    @property
    def stripe_dictionary(self):
        doc = None
        if not self.interval == 0:
            doc = {
                'id': self.stripe_id,
                'name': self.name,
                'amount': convert_to_cents(self.amount),
                'currency': self.currency,
                'interval': self.INTERVAL_CHOICES[self.interval][1],
                'statement_descriptor': Truncator(
                    'IA: {name}'.format(
                        name=self.name
                    )
                ).chars(22)
            }
        return doc


class PlanModule(TimeStamped):
    plan = models.ForeignKey(Plan)
    module = models.ForeignKey(Module)

    class Meta:
        unique_together = ['plan', 'module']
