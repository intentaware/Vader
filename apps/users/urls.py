from django.conf.urls import patterns, include, url

urlpatterns =[
    url(r'^auth/', include('apps.users.backends.urls')),
]
