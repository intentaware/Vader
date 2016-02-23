from django.conf.urls import patterns, include, url
#from django.views.generic.base import TemplateView
from .views import UserRegistrationView, CompanyRegistrationView, \
    PasswordResetEmailView, PasswordResetEmailSentDone, UpdateLostPassword


urlpatterns = [
    url(
        r'^register/$',
        CompanyRegistrationView.as_view(),
        name='registration_register',
    ),
    url(
        r'^password/reset/$',
        PasswordResetEmailView.as_view(),
        name='registration_password_reset',
    ),
    url(r'^password/reset/email/sent/$',
        PasswordResetEmailSentDone.as_view(),
        name='registration_password_reset_done'
    ),
    url(r'^password/reset/(?P<key>\w+)/update/$',
        UpdateLostPassword.as_view(),
        name='update_lost_password'),
    url(r'', include('registration.auth_urls')),
]
