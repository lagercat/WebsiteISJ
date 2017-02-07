from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^event/(?P<slug>[^\.]+)/$', views.event_detail, name='event_detail'),
    url(r'^events_all', views.event_all, name='event_all'),
]
