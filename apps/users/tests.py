from django.test.client import Client
from django.test import TestCase
from models import User
from backends.forms import *
import factory
import requests
from pprint import pprint
from apps.companies.models import *

class UserFactory(factory.Factory):
    class Meta:
        model = User

    first_name = 'Robert'
    last_name = 'Steve'
    email = 'selftest@example.com'
    password = 'password'


class UserTest(TestCase):

    user = UserFactory()
    c = Client()

    def get(self, url, follow=False):
        return self.client.get(url, follow=follow)

    def test_user_login_client(self):
        self.client.login(username=self.user.email, password=self.user.password)


    def test_get_full_name(self):
        full_name = self.user.get_full_name()
        self.assertEqual(full_name, 'Robert Steve')

    def test_get_username(self):
        username = self.user.get_username()
        if username == 'selftest@example.com':
            return True
        else:
            return False

    def test_update_key(self):
        update_key = self.user.update_key()

        print update_key

    def test_get_short_name(self):
        short_name = self.user.get_short_name()
        if short_name == 'Robert Steve':
            return True
        else:
            return False

    def test_send_email(self):
        send_email = self.user.send_email(subject="Test subject", message="Test message")

    def test_send_templated_email(self):
        t_email = self.user.send_templated_email(template= "emails/welcome-email.html",context={'user': self},
            subject="subject")

    def test_send_password_reset_email(self):
        p_email = self.user.send_password_reset_email()

        print p_email

    def test_user_registration_view(self):
        response = self.c.get('/users/auth/register/')
        if response.status_code == 200:
            confirmation  = self.c.post('/users/auth/register/', {'name' : 'SampleName', 'email' : 'selftest@example.com', 'password1' : 'alphanum', 'password2' : 'alphanum'})
            userCheck = User.objects.get(email='selftest@example.com')
            companyCheck = Company.objects.get(name='SampleName')
        else:
            return False
        """
        Password reset url test
        """
        form = self.c.get('/users/auth/password/reset/')
        if form.status_code == 200:
            response = self.c.post('/users/auth/password/reset/',{'email' : 'selftest@example.com'})
            key  = userCheck.update_key()
            print response
            print type(key)



