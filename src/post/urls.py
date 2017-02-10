from django.conf.urls import url
from . import views
from config import settings

urlpatterns = [
    url(r'^media/documents/(?P<location>\w+)/(?P<path>.*)$', views.exterior_files, name="serve"),
    url(r'^submit/', views.upload_file_form, name="submit"),
    url(r'^files/(\d+)/', views.uploaded_files, name="files"),
    url(r'^downloadfile/(?P<slug>[^\.]+)/$', views.download_file, name="download_file"),
    url(r'^deletefile/(?P<slug>[^\.]+)/$', views.delete_file, name="delete_file"),
    url(r'^edit/(?P<slug>[^\.]+)/$', views.edit_file, name="edit_file"),
    url(r'^page/(?P<slug>[^\.]+)/$', views.show_page, name="show_page"), #temp
    url(r'^files_filter/', views.files_filter, name="filter_files"),
    url(r'^add_files/', views.add_multiple_files, name="add_multiple_files"),
    url(r'^preview_page/', views.page_preview, name="preview_page")
]
