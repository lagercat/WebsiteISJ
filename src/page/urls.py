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
    url(r'^category_all/$', views.category_all, name='category_all'),
    url(r'^category/(?P<slug>[^\.]+)/$', views.category, name='category'),
    url(r'^simple/(?P<slug>[^\.]+)/$', views.simple_page_article,
        name='simple'),
    url(r'^subcategory/(?P<slug>[^\.]+)/$', views.subcategory, name='subcategory'),
    url(r'^article/(?P<slug>[^\.]+)/$', views.article_post,
        name='article'),

]
