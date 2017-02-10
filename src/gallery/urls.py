from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^gallery', views.gallery, name='gallery'),
]
