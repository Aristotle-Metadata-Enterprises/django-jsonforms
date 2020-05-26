django-jsonforms
================

.. image:: https://travis-ci.org/Aristotle-Metadata-Enterprises/django-jsonforms.svg?branch=master
    :target: https://travis-ci.org/Aristotle-Metadata-Enterprises/django-jsonforms

django-jsonforms provides a Django integration of json-editor (https://github.com/json-editor/json-editor).
A form field is provided that renders the dynamic form created by json-editor, loading in the provided schema and options along with any initial form data.
The field can be rendered in the same way as any other django field and also validates submitted data against your json schema on submission.

Installation
------------

Install with pip
``pip install django-jsonforms``

Add ``django_jsonforms`` to your INSTALLED_APPS

Make sure you have APP_DIRS set to True in your ``TEMPLATES`` setting. 
More about the templates setting here: https://docs.djangoproject.com/en/2.0/ref/settings/#templates

Requirements
------------

`jQuery <https://jquery.com>`_ is required on the page that will be rendering the form.

Usage
-----

The field can be used like any other Django form field, it has the schema and options attributes which can be either python dictionaries or paths to static files as as shown below

+ The schema parameter is the json schema the field will use
+ The options parameter is passed through to the json-editor object, these options are described here: https://github.com/jdorn/json-editor#options (the schema option is not used)
+ An optional ajax parameter determines whether any files are loaded via ajax on the frontend or loaded in the backend and put into html parameters (defaults to true)

Example::

    from django.forms import ModelForm, Form
    from django_jsonforms.forms import JSONSchemaField

    class RegistrySettingsForm(Form):

        json = JSONSchemaField(
            schema = 'schema/schema.json',
            options = 'schema/options.json'
        )

In this example the schema file would be located in 'static/schema/schema.json'. You will need to run collectstatic after creating the file

To load the file from a directory other than STATIC_ROOT see the ``JSONFORMS_SCHEMA_DIR`` setting below

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

Settings
--------

The ``JSONFORMS_SCHEMA_DIR`` setting can be used to specify the file directory to load the schema from. This directory will need to be seving static files for the form to funciton correctly

The ``JSONFORMS_SCHEMA_VALIDATE`` settings can be set to False to disable backend validation of the submitted json. This can allow a user to submit any json if the frontend validation is bypassed. This settings should only be used during development
