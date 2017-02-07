from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^news/(?P<slug>[^\.]+)/$', views.news, name='news'),
    url(r'^news', views.news_all, name='news'),
]
