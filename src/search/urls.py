from django.conf.urls import url

from . import views


urlpatterns = [
    url(r'^search/$', views.CustomSearchView.as_view(), name='search_view')
]
