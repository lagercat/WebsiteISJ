from django.conf.urls import url
from . import views
from config import settings
from django.views.static import serve
from django.contrib.auth.decorators import login_required

urlpatterns = [
    url(r'^media/(?P<path>.*)$', login_required(serve),{'document_root': settings.MEDIA_ROOT, 'show_indexes': False}),
    url(r'^submit/', views.upload_file_form, name="submit"),
    url(r'^files/(\d+)/', views.uploaded_files, name="files"),
    url(r'^downloadfile/(?P<slug>[^\.]+)/$', views.download_file, name="download_file"),
    url(r'^deletefile/(?P<slug>[^\.]+)/$', views.delete_file, name="delete_file"),
    url(r'^edit/(?P<slug>[^\.]+)/$', views.edit_file, name="edit_file"),
    url(r'^page/(?P<slug>[^\.]+)/$', views.show_page, name="show_page"), #temp
    url(r'^files_filter/', views.files_filter, name="filter_files"),
    url(r'^admin/post/post/add/multiple/', views.add_multiple_files, name="add_multiple_files")
]
