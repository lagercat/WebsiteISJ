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
from config import settings

from django.contrib.admin.views.decorators import staff_member_required
from django.core.paginator import EmptyPage
from django.core.paginator import PageNotAnInteger
from django.core.paginator import Paginator
from django.http.response import HttpResponseForbidden
from django.shortcuts import render

from models import Event


def event_all(request):
    events = Event.objects.order_by('-date')
    print events
    paginator = Paginator(events, 4)

    page = request.GET.get('page')
    try:
        events = paginator.page(page)
    except PageNotAnInteger:
        events = paginator.page(1)
    except EmptyPage:
        events = paginator.page(paginator.num_pages)

    index = events.number - 1
    max_index = len(paginator.page_range)
    start_index = index - 3 if index >= 3 else 0
    end_index = index + 3 if index <= max_index - 3 else max_index
    page_range = list(paginator.page_range)[start_index:end_index]

    return render(request, 'event/events.html', {
        'events': events,
        'page_range': page_range
    })


def event_detail(request, slug):
    articol = list(Event.objects.values('name', 'text', 'date', 'file',
                                        'author__first_name',
                                        'author__last_name', 'address',
                                        'geolocation',
                                        'location',
                                        'slug').filter(slug=slug))
    other_event = Event.objects.all().exclude(slug=slug)[:4]
    return render(request, 'event/event_detail.html', {
        'google_maps_api_key': settings.GOOGLE_MAPS_API_KEY,
        'name': articol[0].get('name'),
        'text': articol[0].get('text'),
        'location': articol[0].get('address'),
        'geolocation': articol[0].get('geolocation'),
        'author': articol[0].get('author__first_name') + " " + articol[0].get(
            'author__last_name'),
        'date': articol[0].get('date'),
        'other_event': other_event,
        'thumbnail': "/media/" + articol[0].get('file'),

    })


@staff_member_required
def event_detail_preview(request):
    if request.method == "GET":
        return render(request, 'event/event_detail.html', {
            'name': "{0}",
            'text': "{1}",
            'author': request.user.get_full_name(),
            'event_location': "{3}",
            'date': "{4}",
            'thumbnail': "{2}",
        })
    else:
        return HttpResponseForbidden()
