from django.test import TestCase
from apps.common.factories import *
from models import *

class FinancesTest(TestCase):
    basePayment = BasePaymentModelFactory()

    def test_amount(self):
        self.assertEqual(self.basePayment.amount, 30.25, "Finances test_amount Failed")
        print "Finances test_amount Passed"

    def test_attempts(self):
        self.assertEqual(self.basePayment.attempts, 3, "Finances test_attempts Failed")
        print "Finances test_attempts Passed"

    def test_service_charges(self):
        self.assertEqual(self.basePayment.service_charges, 10, "Finances test_service_charges Failed")
        print "Finances test_service_charges Passed"

    def test_taxes(self):
        self.assertEqual(self.basePayment.taxes, 17, "Finances test_taxes Failed")
        print "Finances test_taxes Passed"

    def test_gateway_response(self):
        self.assertEqual(self.basePayment.gateway_response, {'status' : 'passed', 'amount' : '30', 'tax' : '17'}, "Finances test_gateway_response Failed")
        print "Finances test_gateway_response Passed"

    def test_is_paid(self):
        self.assertEqual(self.basePayment.is_paid, True, "Finances test_is_paid Failed")
        print "Finances test_is_paid Passed"
