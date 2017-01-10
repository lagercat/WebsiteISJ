from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^subpost/', views.create_subject_post, name="subpost")
]
