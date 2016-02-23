from django.conf.urls import patterns, include, url
from .routes import router

urlpatterns = [
    url('', include(router.urls)),
]
