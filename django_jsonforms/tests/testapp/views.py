from django.views.generic import FormView
from django.forms import Form

from django_jsonforms.forms import JSONSchemaField, JSONSchemaForm
# Forms

class JSONTestForm(Form):

    json = JSONSchemaField(schema='test_schema.json', options={})

# Views

class JSONFormView(FormView):

    template_name="form.html"

    def get_form(self):
        return JSONSchemaForm(schema='test_schema.json', options={})
