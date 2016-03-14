from django.template import Library
from django.core.serializers import serialize
from django.utils.safestring import mark_safe
import json
from decimal import Decimal

register = Library()

class CommonJSONEncoder(json.JSONEncoder):

    """
    Common JSON Encoder
    json.dumps(myString, cls=CommonJSONEncoder)
    """

    def default(self, obj):

        # determine the type of each object and do whatever is
        # requred accordingly
        if isinstance(obj, Decimal):
            return str(obj)

def jsonify(value):
    """
    Takes a python dictionary or list and returns a json,
    not to be used against querysets or complex dictionaries with
    python class objects
    """
    return json.dumps(value, cls=CommonJSONEncoder)

register.filter('jsonify', jsonify)
jsonify.is_safe = True
