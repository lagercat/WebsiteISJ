from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^submit/', views.upload_file_form, name="submit"),
    url(r'^files/', views.uploaded_files, name="files")
]
