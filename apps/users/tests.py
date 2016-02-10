from django.test.client import Client
from django.test import TestCase
from models import User
from backends.forms import *
import requests
from pprint import pprint
from apps.companies.models import *
from apps.common.factories import *




class UserTest(TestCase):

    user = UserFactory()
    c = Client()

    def get(self, url, follow=False):
        return self.client.get(url, follow=follow)

    def test_user_login_client(self):
        self.client.login(username=self.user.email, password=self.user.password)
        print "test_user_login Passed"


    def test_get_full_name(self):
        full_name = self.user.get_full_name()
        self.assertEqual(full_name,"Robert Steve", "User test_get_full_name Failed")
        print "User test_get_full_name"

    def test_get_username(self):
        username = self.user.get_username()
        self.assertEqual(username, "Robert Steve", "User test_get_username Failed")
        print "User test_get_username Passed"
    
    def test_update_key(self):
        update_key = self.user.update_key()
        print "User test_update_key Passed"
    
    def test_get_short_name(self):
        short_name = self.user.get_short_name()
        self.assertEqual(short_name, "Robert Steve", "User test_get_short_name Failed")
        print "User test_get_short_name Passed"
    
    def test_send_email(self):
        send_email = self.user.send_email(subject="Test subject", message="Test message")
        print "User test_send_email Passed"
    """
    def test_send_templated_email(self):
        t_email = self.user.send_templated_email(template= "emails/welcome-email.html",context={'user': self},
            subject="subject")
        print "User test_send_templated_email Passed"

    def test_send_password_reset_email(self):
        p_email = self.user.send_password_reset_email()

        print "User test_send_password_reset_email Passed"
    """
    def test_user_registration_view(self):
        response = self.c.get('/users/auth/register/')
        if response.status_code == 200:
            confirmation  = self.c.post('/users/auth/register/', {'name' : 'SampleName', 'email' : 'selftest@example.com', 'password1' : 'alphanum', 'password2' : 'alphanum'})
            userCheck = User.objects.get(email='selftest@example.com')
            companyCheck = Company.objects.get(name='SampleName')
            key1 = userCheck.key
        else:
            return False
        
        form = self.c.get('/users/auth/password/reset/')
        if form.status_code == 200:
            response = self.c.post('/users/auth/password/reset/',{'email' : 'selftest@example.com'})
            key2  = userCheck.key
            if key1 != key2:
                print "User test_user_registration_view Failed"
                return False
            else:
                print "User test_user_registration_view Passed"
                return True
        
