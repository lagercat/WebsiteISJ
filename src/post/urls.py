from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^media/documents/(?P<location>\w+)/(?P<path>.*)$', views.exterior_files, name="serve"),
    url(r'^page/(?P<slug>[^\.]+)/$', views.show_page, name="show_page"),  # temp
    url(r'^download/(?P<slug>[^\.]+)/$', views.download_interior_file, name="download_interior"),
    url(r'^files_filter/', views.files_filter, name="filter_files"),
    url(r'^add_files/', views.add_multiple_files, name="add_multiple_files"),
    url(r'^preview_page/', views.page_preview, name="preview_page")
]
