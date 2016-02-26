from django.conf.urls import patterns, include, url
from .routes import router
from .views import PostMetric

urlpatterns = [
    url(r'^g/(?P<asset_id>.+)/$', PostMetric.as_view(), name='post_matric'),
    url('', include(router.urls)),
]
