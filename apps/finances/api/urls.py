from django.conf.urls import patterns, include, url
from .routes import router
from .views import invoice_webhook

urlpatterns = [
    url(r'^webhooks/invoices/$', invoice_webhook),
    url('', include(router.urls)),
    ]
