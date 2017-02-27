from django.conf.urls import url
from . import views

urlpatterns = [

    url(r'^schools/(?P<slug>[^\.]+)/$', views.schools, name='schools'),
    url(r'^school_all', views.schools_all, name='schools_all'),
    url(r'^school_map', views.schools_map, name='schools_map')

    ]