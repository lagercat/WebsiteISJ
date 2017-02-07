from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^news/(?P<slug>[^\.]+)/$', views.news, name='news'),
]
