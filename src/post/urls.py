from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^submit/', views.upload_file_form, name="submit"),
    url(r'^files/', views.uploaded_files, name="files"),
    url(r'^downloadfile/(?P<slug>[^\.]+)/$', views.download_file, name="download_file"),
    url(r'^deletefile/(?P<slug>[^\.]+)/$', views.delete_file, name="delete_file"),
    
]
