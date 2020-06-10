from setuptools import setup, find_packages

from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))

__version__ = '1.1.2'

# Get the long description from the README file
with open(path.join(here, 'README.rst'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='django-jsonforms',
    version=__version__,
    description='JSON Schema forms for Django',
    long_description=long_description,
    include_package_data=True,
    url='https://github.com/Aristotle-Metadata-Enterprises/django-jsonforms',
    author='Harry White',
    packages=find_packages(),
    install_requires=['jsonschema','django>=2.0'],
    license='BSD'
)
