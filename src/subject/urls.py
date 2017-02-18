from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^subpost/', views.create_subject_post, name="subpost"),
    url(r'^subject/(?P<name>.+?)/$', views.subject, name='subject'),
    url(r'^subject/(?P<name>.+?)/(?P<slug>[^\.]+)/$', views.subject_news, name='subject_news'),
    url(r'^preview_subjectpost/', views.subject_news_preview, name='subject_news_preview'),
]
