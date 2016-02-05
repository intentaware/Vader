from django.test import TestCase
from apps.common.factories import *
from models import *

class WarehouseTest(TestCase):
    store = IPStoreFactory()

    def test_ip(self):
        self.assertEqual(self.store.ip, "69.89.31.226", "Warehouse test_ip Failed")
        print "Warehouse test_ip Passed"

    def test_latitude(self):
        self.assertEqual(self.store.latitude, 30.1978, "Warehouse test_latitude Failed")
        print "Warehouse test_latitude Passed"

    def test_longitude(self):
        self.assertEqual(self.store.longitude, 71.4697, "Warehouse test_longitude Failed")
        print "Warehouse test_longitude Passed"
