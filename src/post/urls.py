from django.conf.urls import url
from . import views
from config import settings
from django.views.static import serve
from django.contrib.auth.decorators import login_required

urlpatterns = [
    url(r'^media/(?P<path>.*)$', login_required(serve),{'document_root': settings.MEDIA_ROOT, 'show_indexes': False}),
    url(r'^submit/', views.upload_file_form, name="submit"),
    url(r'^files/', views.uploaded_files, name="files"),
    url(r'^downloadfile/(?P<slug>[^\.]+)/$', views.download_file, name="download_file"),
    url(r'^deletefile/(?P<slug>[^\.]+)/$', views.delete_file, name="delete_file"),
    url(r'^edit/(?P<slug>[^\.]+)/$', views.edit_file, name="edit_file")
]
