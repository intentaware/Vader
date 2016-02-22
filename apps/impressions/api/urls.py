from django.conf.urls import patterns, include, url

from .routes import router
from .views import GetImpression, GetProfile

urlpatterns = patterns(
    'impressions',
    #url(r'^register/user/$', UserRegistrationView.as_view(), name='register_user'),
    url('', include(router.urls)),
    url(r'^profile/$', GetProfile.as_view(), name='get_profile'),
    url(r'^i/$', GetImpression.as_view(), name='get_new_impression'),
    #url(r'^i/(?P<pk>\d+)/(?P<email>[\w.%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,4})/$', GetImpression.as_view(), name='claim_coupon'),
    url(r'^i/(?P<pk>\d+)/(?P<b64_string>.+)/$', GetImpression.as_view(), name='process_impression_base64')
)
