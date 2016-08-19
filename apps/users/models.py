from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, \
    PermissionsMixin
from django_extensions.db.fields import ShortUUIDField

from apps.common.models import *


class UserManager(BaseUserManager):
    '''
    methods added to base user manager for easy managing
    '''

    @classmethod
    def normalize_email(cls, email):
        """
        Normalize the address by lowercasing the email and domain of the email
        address.
        """
        email = email or ''
        try:
            email_name, domain_part = email.strip().rsplit('@', 1)
        except ValueError:
            pass
        else:
            email = '@'.join([email_name.lower(), domain_part.lower()])
        return email

    def create_user(self, email=None, password=None, **extra_fields):
        """
        Creates and saves a User with the given email and password.
        """
        email = self.normalize_email(email)
        user = self.model(email=email, is_active=True, **extra_fields)

        if password:
            user.set_password(password)
        else:
            user.set_unusable_password()
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password, **extra_fields):
        """
        Creates and saves a SuperUser with the given email and password.
        """
        u = self.create_user(email, password, **extra_fields)
        u.is_staff = True
        u.is_active = True
        u.is_superuser = True
        u.save(using=self._db)
        return u


class User(TimeStamped, AbstractBaseUser, PermissionsMixin):
    '''
    replacemnt for default auth.User model
    inheriting for AbstractBaseUser for default methods
    inherited fields are 'password', 'last_login'
    inhertited methods are 'is_authenticated', 'is_anonymous',
    'set_password', 'check_password'
    '''

    first_name = models.CharField(max_length=32, blank=True)
    last_name = models.CharField(max_length=32, blank=True)
    email = models.EmailField(
        max_length=128, blank=True,
        null=True, unique=True
    )

    is_active = models.BooleanField(default=True)
    # Dates
    date_joined = CreationDateTimeField()

    # methods
    objects = UserManager()

    # properties
    is_advertiser = models.BooleanField(default=False)
    is_publisher = models.BooleanField(default=False)

    # requirements for django.auth
    USERNAME_FIELD = 'email'

    # The good old django admin
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)

    # activation/reset link
    key = ShortUUIDField(blank=True, null=True)

    def __unicode__(self):
        name = self.email
        if self.first_name or self.last_name:
            name = u'%s %s' % (self.first_name, self.last_name)
        return name

    def get_full_name(self):
        if self.first_name or self.last_name:
            return u'%s %s' % (self.first_name, self.last_name)
        return None

    def get_username(self):
        if self.name:
            return self.name
        return self.email

    @property
    def username(self):
        return self.email

    @property
    def name(self):
        return self.get_full_name()

    @property
    def email_from(self):
        if self.name:
            return '%s <%s>' % (self.name, self.email)
        else:
            return self.email

    def update_key(self):
        import shortuuid
        self.key = shortuuid.uuid()
        self.save()
        self.send_password_reset_email()

    def get_short_name(self):
        return self.get_username()

    def send_email(self, **kwargs):
        """
        Leverage django send_email function to sent email
        "DO NOT send in the from parameter
        """
        from django.core.mail import send_mail
        from django.conf import settings
        send_mail(
            recipient_list=[
                self.email_from,
            ],
            from_email=settings.ADOMATTIC_FROM,
            **kwargs
        )

    def send_templated_email(self, template, context, **kwargs):
        """
        Sends a rendered email and send the email as an html,
        requires a template path and template context to be sent
        """
        #from .tasks import send_templated_email as templated_email
        #templated_email.delay(self.email_from, template, context, **kwargs)
        from django.template.loader import render_to_string
        from django.core.mail import EmailMessage
        from django.conf import settings

        message = render_to_string(template, context)
        email = EmailMessage(
            to=[
                self.email_from,
            ],
            from_email=settings.ADOMATTIC_FROM,
            body=message,
            **kwargs
        )
        email.content_subtype = 'html'
        email.send()

    def send_registration_email(self, **kwargs):
        subject = 'Welcome to IntentAware'
        template = 'emails/welcome-email.html'
        self.send_templated_email(
            template=template,
            context={
                'user': self
            },
            subject=subject,
            **kwargs
        )

    def send_password_reset_email(self, **kwargs):
        subject = '[IntentAware] Reset your password'
        template = 'emails/password-reset.html'
        self.send_templated_email(
            template=template,
            context={
                'user': self
            },
            subject=subject,
            **kwargs
        )


class Visitor(TimeStamped):
    user = models.ForeignKey('users.User', blank=True, null=True)
    key = ShortUUIDField()
    has_opted_out = models.BooleanField(default=False)

    def set_opt_out_flag(self):
        self.has_opted_out = True
        self.save()

    def __unicode__(self):
        return self.key


from signals import *
