from django.conf.urls import include, url
from django_jsonforms.tests import views

urlpatterns = [
    url(r'^testform/', views.JSONFormView.as_view(), name='testform')
]
