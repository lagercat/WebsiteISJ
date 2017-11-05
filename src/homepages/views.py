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
from django.shortcuts import render

from event.models import Event
from gallery.models import Gallery
from news.models import News
from school.models import School
from subject.models import Subject
from editables.models import Editable


def home(request):
    template = 'homepages/index.html'
    noutati = News.objects.all()[:3]
    events = Event.objects.all()[:9]
    subjects = Subject.objects.all()[:6]
    album = Gallery.objects.all()[:3]
    schools = School.objects.all()[:3]
    video_link = Editable.objects.get(editable_type="1").text
    about_us = Editable.objects.get(editable_type="2").text
    welcome = Editable.objects.get(editable_type="3").text
    mission = Editable.objects.get(editable_type="4").text
    return render(request, template, {
        'noutati': noutati,
        'events': events,
        'subjects': subjects,
        'album': album,
        'schools': schools,
        "video_link": video_link,
        "about_us": about_us,
        "welcome": welcome,
        "mission": mission
    })
