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
from django.conf.urls import include, url
from django.contrib import admin

from authentication.views import admin_logout_view

urlpatterns = [
    url(r'^tinymce/', include('tinymce.urls')),
    url(r'^admin/logout', admin_logout_view, name="admin_logout"),
    url(r'^admin/', admin.site.urls),
    url(r'^', include('search.urls')),
    url(r'^', include('homepages.urls')),
    url(r'^', include('authentication.urls')),
    url(r'^', include('post.urls')),
    url(r'^', include('news.urls')),
    url(r'^', include('subject.urls')),
    url(r'^', include('event.urls')),
    url(r'^', include('gallery.urls')),
    url(r'^', include('contact.urls')),
    url(r'^', include('school.urls')),
    url(r'^', include('registration.urls')),
    url(r'^', include('page.urls')),
    url(r'^', include('editables.urls'))
]
