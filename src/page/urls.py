from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^category_all/$', views.category_all, name='category_all'),
    url(r'^category/(?P<slug>[^\.]+)/$', views.category, name='category'),
    url(r'^simple/(?P<slug>[^\.]+)/$', views.simple_page_article,
        name='simple'),
    url(r'^subcategory/(?P<slug>[^\.]+)/$', views.subcategory, name='subcategory'),
    url(r'^article/(?P<slug>[^\.]+)/$', views.article_post,
        name='article'),

]
