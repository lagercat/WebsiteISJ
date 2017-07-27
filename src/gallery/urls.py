# Copyright 2017 Adrian-Ioan Gărovăț, Emanuel Covaci, Sebastian-Valeriu Maleș
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
    url(r'^album', views.gallery, name='gallery'),
    url(r'^gallery/(?P<slug>[^\.]+)/$', views.gallery_img, name='gallery'),
    url(r'^remove_gallery_photo', views.remove_gallery_photo, name='remove_gallery_photo'),
    url(r'^add_gallery', views.add_gallery, name='add_gallery'),

]
