from django.conf.urls import include, url
from django_jsonforms.tests.testapp import views

urlpatterns = [
    url(r'^testform/', views.JSONFormView.as_view(), name='testform'),
    url(r'^testformstatic/', views.JSONFormView.as_view(), name='testformstatic'),
    url(r'^success/', views.success_view, name='success')
]
