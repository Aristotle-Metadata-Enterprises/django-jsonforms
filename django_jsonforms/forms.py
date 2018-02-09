from django import forms
from django.forms import fields, ValidationError
from django.forms.widgets import Textarea, Widget
import jsonschema
from jsonfield.fields import JSONFormField
import json

class JSONEditorWidget(Widget):

    template_name = 'django_jsonforms/jsoneditor.html'

    class Media:
        js = ('django_jsonforms/jsoneditor.min.js', 'django_jsonforms/jsoneditor_init.js')

    def __init__(self, schema, options, *args, **kwargs):
        super(JSONEditorWidget, self).__init__(*args, **kwargs)
        self.schema = schema
        self.options = options

    def get_context(self, name, value, attrs):
        context = super(JSONEditorWidget, self).get_context(name, value, attrs)
        context.update({'schema': json.dumps(self.schema), 'options': json.dumps(self.options)})
        context['widget']['type'] = 'hidden'
        return context

class JSONSchemaField(JSONFormField):

    def __init__(self, schema, options, *args, **kwargs):
        super(JSONSchemaField, self).__init__(*args, **kwargs)
        self.schema = schema
        self.widget = JSONEditorWidget(schema=schema, options=options)

    def clean(self, value):
        value = super(JSONSchemaField, self).clean(value)

        try:
            jsonschema.validate(value, self.schema)
        except jsonschema.exceptions.ValidationError as e:
            raise ValidationError(message=e.message)

        return value

class JSONSchemaForm(forms.Form):

    def __init__(self, schema, options, *args, **kwargs):
        super(JSONSchemaForm, self).__init__(*args, **kwargs)
        self.fields['json'] = JSONSchemaField(schema=schema, options=options)
