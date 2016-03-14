from rest_framework.exceptions import ValidationError
from django.utils import timezone


class StripeCardValidator(object):
    '''
    Generic Stripe Validator to be called on Serializer Object.
    '''
    def __init__(self, klass, *args, **kwargs):
        '''
        the initializing requires a serializer upon which the validator
        is being set

        Params:
            klass - defines the model object upon which the serializer is set
        '''
        self.message = None
        self.klass = klass

    def set_context(self, serializer):
        if type(self.klass) is str:
            self.klass = getattr(serializer, 'klass', None)

    def __call__(self, attrs):
        import math

        amount = attrs.pop('amount', None)
        cents, dollars = math.modf(amount)

        # converting to cents
        cents = (int(dollars) * 100) + int(cents * 100)

        self.klass._params = {
            "source": attrs,
        }
        # why is the currency hard coded here?

        charge, response = self.klass.charge(amount_in_cents=cents,
            description='Invoice #%s' %(self.klass.id))

        if charge:
            self.klass.charged_on = timezone.now()
            self.klass.is_paid = True
            self.klass.gateway_response = response
            self.klass.save()
        if not charge:
            raise ValidationError(response.message)
