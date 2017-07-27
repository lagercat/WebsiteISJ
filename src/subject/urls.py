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

    url(r'^subject_page_all/$', views.subject_page_all, name="suba_page_all"),

    url(r'^subpost/$', views.create_subject_post, name="subpost"),

    url(r'^subject/(?P<name>.+?)/(?P<kind>.+?)/(?P<slug>[^\.]+)$',
        views.subcategory_subject_news,
        name='subcategory_subject_news'),

    url(r'^subject/(?P<name>.+?)/(?P<kind>.+?)/$', views.subcategory_subject,
        name='subcategory_subject'),

    url(r'^subject/(?P<name>.+?)/$', views.subject, name='subject'),

    url(r'^preview_subjectpost/$', views.subject_news_preview,
        name='subject_news_preview'),

    url(r'^subject/(?P<name>.+?)/(?P<slug>[^\.]+)/$', views.subject_news,
        name='subject_news'),

    url(r'^simple/(?P<name>.+?)/(?P<slug>[^\.]+)/$', views.subject_news,
        name='subject_news'),
]
