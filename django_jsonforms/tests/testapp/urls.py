from django.conf.urls import url
from django_jsonforms.tests.testapp import views

urlpatterns = [
    url(r'^testform/', views.JSONFormView.as_view(), name='testform'),
    url(r'^testformstatic/', views.JSONFormViewStatic.as_view(), name='testformstatic'),
    url(r'^testformdouble/', views.JSONFormViewDouble.as_view(), name='testformdouble'),
    url(r'^success/', views.success_view, name='success')
]
