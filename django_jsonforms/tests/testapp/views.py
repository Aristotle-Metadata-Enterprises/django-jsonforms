from django.views.generic import FormView
from django.forms import Form
from django.http import HttpResponse
from django.urls import reverse

from django_jsonforms.forms import JSONSchemaField

# Forms


class JSONTestFormStatic(Form):
    json = JSONSchemaField(schema='test_schema.json', options={})


class JSONTestFormDouble(Form):

    json1 = JSONSchemaField(schema='test_schema.json', options={})
    json2 = JSONSchemaField(schema='test_schema.json', options={})


class JSONTestForm(Form):

    json = JSONSchemaField(
        schema={
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
        },
        options={}
    )

# Views


class JSONFormView(FormView):

    template_name = "form.html"
    form_class = JSONTestForm

    def get_success_url(self):
        return reverse('success')


class JSONFormViewStatic(FormView):
    template_name = "form.html"
    form_class = JSONTestFormStatic

    def get_success_url(self):
        return reverse('success')


class JSONFormViewDouble(FormView):
    template_name = "form.html"
    form_class = JSONTestFormDouble

    def get_success_url(self):
        return reverse('success')


def success_view(request):
    return HttpResponse('<p id=\"success\">Success</p>')
