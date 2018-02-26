from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^primary_school/$', views.primary_school, name='primary'),
    url(r'^school_registration_detail/(?P<slug>[^\.]+)/$', views.school_registration_detail, name='detail_registration'),
    url(r'^pre_school/$', views.pre_school, name='pre-school'),
]