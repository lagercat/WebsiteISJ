from django.conf.urls import url
from . import views

urlpatterns = [

    url(r'^category/(?P<name>.+?)/$', views.category, name='category'),
    url(r'^simple/(?P<slug>[^\.]+)/$', views.simple_page_article,
        name='simple'),
    url(r'^(?P<name>.+?)/(?P<slug>[^\.]+)/$', views.article_post,
        name='article'),
    url(r'^(?P<name>.+?)/$', views.subcategory, name='subcategory'),


]
