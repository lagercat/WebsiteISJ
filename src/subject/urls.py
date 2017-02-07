from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^subpost/', views.create_subject_post, name="subpost"),
    url(r'^subject/(?P<name>\w+)/$', views.subject, name='subject'),
    url(r'^(?P<name>\w+)/(?P<slug>\w+)/$', views.subject_news, name='subject_news'),
]
