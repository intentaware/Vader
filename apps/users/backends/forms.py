from django import forms
from apps.finances.forms import BasePaymentForm
from apps.users.models import User
from apps.companies.models import Company



class PasswordValidationForm(forms.Form):
    password1 = forms.CharField(
        label='Password',
        widget=forms.PasswordInput)
    password2 = forms.CharField(
        label='Password confirmation',
        widget=forms.PasswordInput)

    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password1 and password2 and password1 != password2:
            msg = 'Passwords mismatch'
            raise forms.ValidationError('Password mismatch')
        return password2


class UserCreationForm(PasswordValidationForm):
    # create user
    email = forms.EmailField(required=True, max_length=128,
        label='Email Address')

    def clean_email(self):
        email = self.cleaned_data.get('email')
        try:
            user = User.objects.get(email=email)
            raise forms.ValidationError('User with this email already exists')
        except User.DoesNotExist:
            return email.lower()


class CompanyCreationForm(UserCreationForm):
    name = forms.CharField(required=True, max_length=128, label='Company Name')


class PasswordResetForm(forms.Form):
    email = forms.EmailField(required=True, max_length=128,
        label='Email Address')

    def clean_email(self):
        email = self.cleaned_data.get('email')

        try:
            user = User.objects.get(email=email)
            self.user = user
        except User.DoesNotExist:
            raise forms.ValidationError('User with this email does not exist')

        self.user = user
        return email

class SubscriptionForm(BasePaymentForm):
    plan = forms.HiddenInput()
    invoice = forms.HiddenInput()

    def clean(self):
        cleaned = super(SubscriptionForm, self).clean()
