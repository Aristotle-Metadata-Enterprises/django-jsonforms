django-jsonforms
================

django-jsonforms provides the JSONSchemaField which renders a dynamic form from a json schema using json-editor (https://github.com/jdorn/json-editor)
The field also validates submitted data against the json schema

Installation
------------


  pip install git+https://github.com/Aristotle-Metadata-Enterprises/django-jsonforms#egg=django-jsonforms

Add 'django_jsonforms' to your INSTALLED_APPS

Requirements
------------

The python requirements jsonschema and django will be installed when installing the package through pip\
Additionally jQuery is required on the page that will be rendering the form. Instructions for adding jQuery here: https://www.w3schools.com/jquery/jquery_get_started.asp

Usage
-----

The field can be used like any other Django form field, it has the schema and options attributes which can be either python dictionaries or paths to staticfiles as as shown below\
The schema parameter is the json schema the field will use\
The options parameter is passed through to the json-editor object, these options are described here: https://github.com/jdorn/json-editor#options (the schema option is not used)\
An optional ajax parameter determines whether any files are loaded via ajax on the frontend or loaded in the backend and put into html parameters (defaults to true)

Example::

    from django.forms import ModelForm, Form
    from django_jsonforms.forms import JSONSchemaField

    class RegistrySettingsForm(Form):

        json = JSONSchemaField(
            schema = 'schema/schema.json',
            options = 'schema/options.json'
        )

In this example the schema file would be located in 'static/schema/schema.json'. You will need to run collectstatic after creating the file

Example showing all options::

    class RegistrySettingsForm(Form):

        json = JSONSchemaField(
            schema = 'schema/schema.json',
            options = {"theme": "bootstrap3"},
            ajax = false
        )

Since it is common to have only one field in this type of form. A form with a single JSONSchemaField named json is also available to use

Form Example::
    from django_jsonforms.forms import JSONSchemaForm

    form = JSONSchemaForm(schema=... , options=... , ajax=...)

Note:

When rendering the form don't forget to render the forms media with the template tag {{ form.media }}. This is required for the field to function correctly

The data returned when the field is submitted is in the form of a python dictionary. This may need to be converted before being stored depending on the model field being used
