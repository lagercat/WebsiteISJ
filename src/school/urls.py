from django.conf.urls import url
from . import views

urlpatterns = [

    url(r'^schools_detail/(?P<slug>[^\.]+)/$', views.school_detail, name='school_detail'),
    url(r'^schools', views.school_all, name='schools'),


    ]