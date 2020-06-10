from django.test import TestCase, override_settings
from django.forms import Form
from django_jsonforms.forms import JSONSchemaField, JSONSchemaForm
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.conf import settings
from selenium.webdriver.firefox.webdriver import WebDriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import json
import os
from unittest import skipUnless

thisdir = os.path.dirname(os.path.dirname(__file__))


class JSONTestForm(Form):

    def __init__(self, schema, options, ajax=True, *args, **kwargs):
        super(JSONTestForm, self).__init__(*args, **kwargs)
        self.fields['json1'] = JSONSchemaField(schema=schema, options=options, ajax=ajax)
        self.fields['json2'] = JSONSchemaField(schema=schema, options=options, ajax=ajax)


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

        self.test_json = {
            'color': 'red',
            'number': 1,
            'list': [
                'very',
                'good',
                'list'
            ]
        }

    def test_valid_data_for_schema(self):

        form_data = {'json': json.dumps(self.test_json)}
        form = JSONSchemaForm(schema=self.schema, options=self.options, data=form_data)
        self.assertTrue(form.is_valid())

    def test_render_valid_data(self):

        form_data = {'json': json.dumps(self.test_json)}
        form = JSONSchemaForm(schema=self.schema, options=self.options, data=form_data)
        output = form.as_p()

        # Check that div with class editor_holder was rendered
        self.assertNotEqual(output.find('class=\"editor_holder\"'), -1)

        media = str(form.media)

        # Check that the media was included correctly
        self.assertNotEqual(media.find('jsoneditor.min.js'), -1)
        self.assertNotEqual(media.find('jsoneditor_init.js'), -1)

    def test_valid_data_for_schema_two_fields(self):

        form_data = {'json1': json.dumps(self.test_json), 'json2': json.dumps(self.test_json)}
        form = JSONTestForm(schema=self.schema, options=self.options, data=form_data)
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

    @override_settings(JSONFORMS_SCHEMA_VALIDATE=False)
    def test_no_validate_setting(self):

        test_json = {
            'color': 'red',
            'number': 'one',
        }
        form_data = {'json': json.dumps(test_json)}
        form = JSONSchemaForm(schema=self.schema, options=self.options, data=form_data)
        self.assertTrue(form.is_valid())

    def test_invalid_schema_file(self):

        form = JSONSchemaForm(options=self.options, schema='very/real/file.json')
        self.assertFalse(form.is_valid())

    @override_settings(STATIC_ROOT=thisdir)
    def test_valid_data_with_schema_file(self):

        form_data = {'json': json.dumps(self.test_json)}
        form = JSONSchemaForm(schema='tests/testapp/staticfiles/test_schema.json', options=self.options, data=form_data)
        self.assertTrue(form.is_valid())

    @override_settings(JSONFORMS_SCHEMA_DIR=thisdir)
    def test_valid_data_with_schema_file_dir_setting(self):

        form_data = {'json': json.dumps(self.test_json)}
        form = JSONSchemaForm(schema='tests/testapp/staticfiles/test_schema.json', options=self.options, data=form_data)
        self.assertTrue(form.is_valid())


@skipUnless(settings.SELENIUM_TEST, "Selenium tests not requested")
class JSONFormsLiveTest(StaticLiveServerTestCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.selenium = WebDriver()
        cls.selenium.implicitly_wait(10)
        cls.wait = WebDriverWait(cls.selenium, 10)

    @classmethod
    def tearDownClass(cls):
        cls.selenium.quit()
        super().tearDownClass()

    def fill_form(self, field_name, add_button_number):

        self.selenium.find_element_by_name(field_name + '[color]').send_keys('blue')
        self.selenium.find_element_by_name(field_name + '[number]').send_keys('100')
        button_xpath = "(//button[@class=' json-editor-btn-add '])[" + str(add_button_number) + "]"
        add_item_button = self.selenium.find_element_by_xpath(button_xpath)
        add_item_button.click()
        self.selenium.find_element_by_name(field_name + '[list][0]').send_keys('Item1')
        add_item_button.click()
        self.selenium.find_element_by_name(field_name + '[list][1]').send_keys('Item2')

    def submit_single_form(self, url):
        # Load form
        self.selenium.get(self.live_server_url + url)

        # Fill form
        self.fill_form('json', 2)

        # Submit form
        self.selenium.find_element_by_id('submit_button').click()

        # Check success
        self.wait.until(EC.visibility_of_element_located((By.ID, 'success')))
        self.assertEqual(self.selenium.current_url, self.live_server_url + '/success/')

    def test_single(self):
        self.submit_single_form('/testform')

    def test_single_static(self):
        self.submit_single_form('/testformstatic')

    def test_double(self):

        self.selenium.get(self.live_server_url + '/testformdouble')

        # Fill both forms
        self.fill_form('json1', 2)
        self.fill_form('json2', 4)

        # Submit form
        self.selenium.find_element_by_id('submit_button').click()

        # Check success
        self.wait.until(EC.visibility_of_element_located((By.ID, 'success')))
        self.assertEqual(self.selenium.current_url, self.live_server_url + '/success/')
