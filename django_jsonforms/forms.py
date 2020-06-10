from django import forms
from django.forms import fields, ValidationError
from django.forms.widgets import Widget
import jsonschema
import os
from django.conf import settings

import json


class JSONEditorWidget(Widget):

    template_name = 'django_jsonforms/jsoneditor.html'

    class Media:
        js = (
            'https://cdn.jsdelivr.net/npm/@json-editor/json-editor@1.3.5/dist/jsoneditor.min.js',
            'django_jsonforms/jsoneditor_init.js'
        )

    def __init__(self, schema, options, *args, **kwargs):
        super(JSONEditorWidget, self).__init__(*args, **kwargs)
        self.schema = schema
        self.options = options

    def get_json_url(self, value, name):
        if isinstance(value, dict):
            return {name: json.dumps(value)}
        else:
            urlname = name + '_url'
            return {urlname: value}

    def get_context(self, name, value, attrs):
        context = super(JSONEditorWidget, self).get_context(name, value, attrs)

        update = self.get_json_url(self.schema, 'schema')
        context.update(update)
        update = self.get_json_url(self.options, 'options')
        context.update(update)

        context['widget']['type'] = 'hidden'
        return context


class JSONSchemaField(fields.CharField):

    def __init__(self, schema, options, ajax=True, *args, **kwargs):
        super(JSONSchemaField, self).__init__(*args, **kwargs)

        self.schemadir = getattr(settings, 'JSONFORMS_SCHEMA_DIR', settings.STATIC_ROOT)
        self.backvalidate = getattr(settings, 'JSONFORMS_SCHEMA_VALIDATE', True)

        self.schema = self.load(schema)

        if (ajax):
            self.widget = JSONEditorWidget(schema=schema, options=options)
        else:
            self.options = self.load(options)
            self.widget = JSONEditorWidget(schema=self.schema, options=self.options)

    def load(self, value):
        if isinstance(value, dict):
            return value
        elif isinstance(value, str):
            file_path = os.path.join(self.schemadir, value)
            if os.path.isfile(file_path):
                static_file = open(file_path, 'r')
                json_value = json.loads(static_file.read())
                static_file.close()
                return json_value

            return None

    def to_python(self, value):
        if isinstance(value, str):
            try:
                return json.loads(value)
            except json.JSONDecodeError:
                raise ValidationError('Invalid JSON')
        return value

    def clean(self, value):

        value = super(JSONSchemaField, self).clean(value)

        if self.backvalidate:
            try:
                jsonschema.validate(value, self.schema)
            except jsonschema.exceptions.ValidationError as e:
                raise ValidationError(message=e.message)

        return value

    def prepare_value(self, value):
        if isinstance(value, dict):
            return json.dumps(value)
        return value


class JSONSchemaForm(forms.Form):

    def __init__(self, schema, options, ajax=True, *args, **kwargs):
        super(JSONSchemaForm, self).__init__(*args, **kwargs)
        self.fields['json'] = JSONSchemaField(schema=schema, options=options, ajax=ajax)
