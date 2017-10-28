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

from django.core.paginator import EmptyPage
from django.core.paginator import PageNotAnInteger
from django.core.paginator import Paginator
from django.shortcuts import render

from models import School


def schools_all(request):
    all_schools = School.objects.all()
    school_first = all_schools[:len(all_schools) / 2]
    school_second = all_schools[len(all_schools) / 2:]
    school_pair = zip(school_first, school_second)
    if len(all_schools) % 2 == 1:
        school_pair.append((school_second[-1], None))

    paginator = Paginator(school_pair, 4)
    page = request.GET.get('page')
    try:
        all_schools = paginator.page(page)
    except PageNotAnInteger:
        all_schools = paginator.page(1)
    except EmptyPage:
        all_schools = paginator.page(paginator.num_pages)
    return render(request, 'school/school_all.html', {
        'schools': all_schools,
    })


def schools_map(request):
    school = School.objects.all().order_by('name')
    return render(request, 'school/school_map.html', {
        'google_maps_api_key': settings.GOOGLE_MAPS_API_KEY,
        'schools': school,
    })


def schools(request, slug):
    articol = list(
        School.objects.values('name', 'telephone', 'fax', 'email', 'website',
                              'address',
                              'geolocation', 'file','type_school').filter(
            slug=slug))
    other_schools = School.objects.all().exclude(slug=slug)[:4]
    school = {
        0:'Gradinita',
        1:'Scoala Gimnaziala',
        2: 'Liceu'
    }
    return render(request, 'school/school_detail.html', {
        'google_maps_api_key': settings.GOOGLE_MAPS_API_KEY,
        'name': articol[0].get('name'),
        'telephone': articol[0].get('telephone'),
        'fax': articol[0].get('fax'),
        'email': articol[0].get('email'),
        'website': articol[0].get('website'),
        'location': articol[0].get('address'),
        'geolocation': articol[0].get('geolocation'),
        'type': school[articol[0].get('type_school')],
        'other_news': other_schools,
        'thumbnail': "/media/" + articol[0].get('file'),

    })
