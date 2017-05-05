from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^news/(?P<slug>[^\.]+)/$', views.news, name='news'),
    url(r'^news_all', views.news_all, name='news_all'),
    url(r'^preview_news/', views.news_preview, name='news_preview'),
]
