from django.test import TestCase
from models import Company
from apps.campaigns.models import *
from apps.common.factories import *

class CompaniesTest(TestCase):
    company = CompaniesFactory()
    campaign = CampaignFactory()

    def test_is_active(self):
        self.assertEqual(self.company.is_active, True, "Company is_active test Failed.")
        print "Company is_active test Passed"

    def test_is_advertiser(self):
        self.assertEqual(self.company.is_advertiser, True, "Company is_advertiser test Failed.")
        print "Company is_advertiser test Passed."

    def test_publisher_key(self):
        self.assertEqual(self.company.publisher_key, "YufjaydQ_U2NQ2Qq8kogKA", "Company publisher_key test Failed")
        print "Company publisher_key test Passed"

    def test_advertiser_rate(self):
        self.assertEqual(self.company.advertiser_rate, 1.045, "Company advertiser_rate test Failed")
        print "Company advertiser_rate test Passed"

    def test_payment_data(self):
        self.assertEqual(self.company.payment_data, {'method' : 'bank', 'bank_name' : 'citi', 'acc_no' : '04596'}, "Company payment_data test Failed")
        print "Company payment_data test Passed"

    def test_get_target_campaigns(self):
        response = self.company.get_target_campaigns(request='GET',campaign_id=self.campaign.id)
        count  = Coupon.objects.all().count()
        companies = Campaign.objects.all().count()

        print self.campaign.invoice
        
       
