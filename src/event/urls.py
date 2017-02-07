from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^event/(?P<slug>[^\.]+)/$', views.event, name='event'),
    url(r'^event', views.news_all, name='event'),
]
