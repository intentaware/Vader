from django.conf.urls import patterns, include, url

from .views import UserRegistrationView, CompanyRegistrationView, LeadRegistrationView

urlpatterns = [
    url(r'^register/user/$', UserRegistrationView.as_view(), name='register_user'),
    url(r'^register/company/$', CompanyRegistrationView.as_view(), name='register_company'),
    url(r'^register/lead/$', LeadRegistrationView.as_view(), name='register_lead'),
]


