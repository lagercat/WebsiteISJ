from django.conf.urls import url
from . import views

urlpatterns = [

    url(r'^subject_page_all/$', views.subject_page_all, name="suba_page_all"),

    url(r'^subpost/$', views.create_subject_post, name="subpost"),

    url(r'^subject/(?P<name>.+?)/(?P<kind>.+?)/(?P<slug>[^\.]+)$',
        views.subcategory_subject_news,
        name='subcategory_subject_news'),

    url(r'^subject/(?P<name>.+?)/(?P<kind>.+?)/$', views.subcategory_subject,
        name='subcategory_subject'),

    url(r'^subject/(?P<name>.+?)/$', views.subject, name='subject'),

    url(r'^preview_subjectpost/$', views.subject_news_preview,
        name='subject_news_preview'),

    url(r'^subject/(?P<name>.+?)/(?P<slug>[^\.]+)/$', views.subject_news,
        name='subject_news'),

    url(r'^simple/(?P<name>.+?)/(?P<slug>[^\.]+)/$', views.subject_news,
        name='subject_news'),
]
