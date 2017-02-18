from django.conf.urls import url
from . import views

urlpatterns = [

    url(r'^category/(?P<name>.+?)/$', views.category, name='category'),

]
