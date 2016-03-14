from django.conf.urls import patterns, include, url
from django.contrib import admin
from .settings import ADMIN_SITE_HEADER

admin.site.site_header = ADMIN_SITE_HEADER

urlpatterns = [
    # Examples:
    # url(r'^$', 'adomattic.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    # url(r'^grappelli/', include('grappelli.urls')),
    url(r'^admin/', include(admin.site.urls)),
    #url(r'^photologue/', include('photologue.urls', namespace='photologue')),
    # adomattic urls
    url(r'^$', 'apps.dashboard.views.redirect_to_dashboard', name='landing'),
    url(r'^api/', include('apps.api.urls', namespace='api')),
    url(r'^users/', include('apps.users.urls')),
    url(r'^dashboard/', include('apps.dashboard.urls')),
    #url(r'^search/', include('haystack.urls')),
    ]

from django.conf import settings

if settings.DEBUG:
    from django.conf.urls.static import static
    urlpatterns += static('/media/', document_root=settings.MEDIA_ROOT)
