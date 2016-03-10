from django import forms
from apps.finances.forms import BasePaymentForm
from apps.users.models import User
from apps.companies.models import Company, CompanySubscription
from apps.finances.models import Plan



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
    name = forms.CharField(max_length=128, required=True, label='Name on Card')
    plan = forms.IntegerField(widget=forms.HiddenInput(), required=True)

    def clean(self):
        cleaned = super(SubscriptionForm, self).clean()

        if not self.errors:
            card = dict()
            card['object'] = 'card'
            card['name'] = self.cleaned_data['name']
            card['number'] = self.cleaned_data['number']
            card['cvc'] = self.cleaned_data['cvc']
            card['exp_month'] = self.cleaned_data['expiration'].month
            card['exp_year'] = self.cleaned_data['expiration'].year

            company = getattr(self, 'company', None)
            customer = company.stripe_customer
            customer.source = card

            try:
                customer.save()
            except (company._stripe.error.CardError, company._stripe.error.AuthenticationError) as ce:
                if ce.param in ['exp_month', 'exp_year']:
                    self.add_error('expiration', ce.message)
                elif ce.param in ['name', 'cvc']:
                    self.add_error(ce.param, ce.message)
                else:
                    self.add_error('number', ce.message)

            plan = Plan.objects.get(id=self.cleaned_data['plan'])
            try:
                subscription = customer.subscriptions.create(plan=plan.stripe_id)
                CompanySubscription.objects.create(
                    company=company, plan=plan, stripe_id=subscription.id)
            except (company._stripe.error.CardError, company._stripe.error.AuthenticationError, company._stripe.error.InvalidRequestError) as ce:
                self.add_error('number', ce.message)
        else:
            print self.errors
