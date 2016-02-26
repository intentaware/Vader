from django.conf.urls import patterns, include, url


urlpatterns = [
    url(r'^users/', include('apps.users.api.urls')),
    url(r'^campaigns/', include('apps.campaigns.api.urls')),
    url(r'^impressions/', include('apps.impressions.api.urls')),
    url(r'^companies/', include('apps.companies.api.urls')),
    url(r'^finances/', include('apps.finances.api.urls')),
    url(r'^metas/', include('apps.metas.api.urls')),
    url(r'^cities/', include('plugins.cities.api.urls')),
    url(r'^guages/', include('apps.guages.api.urls')),
]
