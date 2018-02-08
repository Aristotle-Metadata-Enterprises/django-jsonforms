from django import forms
from django.forms import fields, ValidationError
from django.forms.widgets import Textarea
import jsonschema
from jsonfield.fields import JSONFormField
import json

class JSONSchemaField(JSONFormField):

    widget = Textarea

    def __init__(self, schema, *args, **kwargs):
        super(JSONSchemaField, self).__init__(*args, **kwargs)
        self.schema = schema

    # maybe add this as a validator instead
    def clean(self, value):
        value = super(JSONSchemaField, self).clean(value)

        try:
            jsonschema.validate(value, self.schema)
        except jsonschema.exceptions.ValidationError as e:
            raise ValidationError(message=e.message)

        return value
