from django import forms
from django.forms import fields, ValidationError
from django.forms.widgets import Textarea, Widget
import jsonschema
from jsonfield.fields import JSONFormField
import json

class JSONEditorWidget(Widget):

    template_name = 'django_jsonforms/jsoneditor.html'

class JSONSchemaField(JSONFormField):

    widget = Textarea

    def __init__(self, schema, *args, **kwargs):
        super(JSONSchemaField, self).__init__(*args, **kwargs)
        self.schema = schema

    def clean(self, value):
        value = super(JSONSchemaField, self).clean(value)

        try:
            jsonschema.validate(value, self.schema)
        except jsonschema.exceptions.ValidationError as e:
            raise ValidationError(message=e.message)

        return value

class JSONSchemaForm(forms.Form):

    def __init__(self, schema, *args, **kwargs):
        super(JSONSchemaForm, self).__init__(*args, **kwargs)
        self.schema = schema
        self.fields['json'] = JSONSchemaField(schema=self.schema)
