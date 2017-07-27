# Copyright 2017 Adrian-Ioan Garovat, Emanuel Covaci, Sebastian-Valeriu Males
#
# This file is part of WebsiteISJ
#
# WebsiteISJ is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# WebsiteISJ is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with WebsiteISJ.   If not, see <http://www.gnu.org/licenses/>.
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
