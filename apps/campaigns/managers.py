from django.db.models import Manager, QuerySet, Sum
from django.utils import timezone as _tz


class CampaignQuerySet(QuerySet):
    """
    custom manager for 'Campaign' model
    """
    def active(self):
        return self.filter(ends_on__gte=_tz.now())

    def active_budget(self):
        return self.aggregate(Sum('budget'))['budget__sum']

    def inactive(self):
        return self.filter(is_active=False, ends_on__lte=_tz.now())


class CampaignManager(Manager):
    use_for_related_fields = True

    def expire(self):
        return self.filter(
            is_active=True, ends_on__lt=_tz.now()
            ).update(is_active=False)


class CouponQuerySet(QuerySet):
    def active(self):
        """
        only get coupons from active campaigns
        """
        return self.filter(campaign__is_active=True)

    def claimed(self):
        """
        get claimed coupons
        """
        return self.filter(claimed_on__isnull=False)

    def remaining(self):
        """
        get coupons that are not claimed
        """
        return self.filter(claimed_on__isnull=True)

    def coupons_value_sum(self):
        sum = self.aggregate(Sum('value'))['value__sum']
        if sum:
            return sum
        else:
            return 0


class CouponManager(Manager):
    use_for_related_fields = True

    def generate(self, campaign, count):
        c = 0
        while c < count:
            self.create(
                    campaign = campaign,
                    company = campaign.company,
                    value = campaign.coupon_value
                )
            c += 1
