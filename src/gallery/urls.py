from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^gallery', views.gallery, name='gallery'),
    url(r'^remove_gallery_photo', views.remove_gallery_photo, name='remove_gallery_photo'),
    url(r'^add_gallery', views.add_gallery, name='add_gallery'),
]
