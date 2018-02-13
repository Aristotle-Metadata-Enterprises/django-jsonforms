from django.test import TestCase
from django.forms import ValidationError
from django_jsonforms.forms import JSONSchemaField, JSONSchemaForm
import json

class DjangoFormsTest(TestCase):

    def setUp(self):
        self.schema = {
            'type': 'object',
            'properties': {
                'color': {
                    'description': 'a color',
                    'type': 'string'
                },
                'number': {
                    'description': 'a very nice number',
                    'type': 'integer'
                },
                'list': {
                    'description': 'what a list',
                    'type': 'array',
                    'items': {
                        'type': 'string'
                    }
                }
            }
        }

        self.options = {'theme': 'html'}

    def test_valid_data_for_schema(self):

        test_json = {
            'color': 'red',
            'number': 1,
            'list': [
                'very',
                'good',
                'list'
            ]
        }
        form_data = {'json': json.dumps(test_json)}
        form = JSONSchemaForm(schema=self.schema, options=self.options, data=form_data)
        self.assertTrue(form.is_valid())

    def test_invalid_json(self):

        form_data = {'json': '{\"yeah\": \"yeah}'}
        form = JSONSchemaForm(schema=self.schema, options=self.options, data=form_data)

        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['json'], [u"Invalid JSON"])

    def test_invalid_data_for_schema(self):

        test_json = {
            'color': 'red',
            'number': 'one',
        }
        form_data = {'json': json.dumps(test_json)}
        form = JSONSchemaForm(schema=self.schema, options=self.options, data=form_data)

        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['json'], [u"\'one\' is not of type \'integer\'"])

# Test file and dict options, file does not exist
