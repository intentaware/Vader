from django.test import TestCase
from models import models
from apps.common.factories import *


class GuagesTese(TestCase):
    asset = AssetFactory()

    def test_name(self):
        self.assertEqual(self.asset.name, "Assests Name", "Guages test_name is Failed")
        print "Guages test_name is passed"

    def test_url(self):
        self.assertEqual(self.asset.url, "www.whatever.com/", "Guages test_url is Failed")
        print "Guages test_url is passed"

    def test_key(self):
        self.assertEqual(self.asset.key, "Xyshje12HjTv", "Guages test_key is Failed")
        print "Guages test_key is passed"

