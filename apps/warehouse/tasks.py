from __future__ import absolute_import
from adomattic.celery import app as capp

@capp.task
def update_ipstore(impression_id):
    from apps.impressions.models import Impression
    imp = Impression.objects.get(id=impression_id)
    meta = imp[meta]
