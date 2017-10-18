from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^primary_school/$', views.primary_school, name='primary'),
    url(r'^pre_school/$', views.pre_school, name='pre-school'),
]