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
from django.contrib.admin.views.decorators import staff_member_required
from django.core.paginator import EmptyPage
from django.core.paginator import PageNotAnInteger
from django.core.paginator import Paginator
from django.http.response import HttpResponseForbidden
from django.shortcuts import render

from models import News


def news_all(request):
    all_news = News.objects.order_by("-date")
    paginator = Paginator(all_news, 6)

    page = request.GET.get('page')
    try:
        all_news = paginator.page(page)
    except PageNotAnInteger:
        all_news = paginator.page(1)
    except EmptyPage:
        all_news = paginator.page(paginator.num_pages)

    index = all_news.number - 1
    max_index = len(paginator.page_range)
    start_index = index - 3 if index >= 3 else 0
    end_index = index + 3 if index <= max_index - 3 else max_index
    page_range = list(paginator.page_range)[start_index:end_index]

    return render(request, 'news/news_all.html', {
        'news_all': all_news,
        'page_range': page_range
    })


def news(request, slug):
    articol = list(News.objects.values('name', 'text', 'author__first_name',
                                       'author__last_name', 'file', 'date',
                                       'slug').filter(slug=slug))
    other_news = News.objects.all().exclude(slug=slug)[:4]
    return render(request, 'news/news.html', {

        'name': articol[0].get('name'),
        'text': articol[0].get('text'),
        'author': articol[0].get(
            'author__first_name') + " " + articol[0].get('author__last_name'),
        'date': articol[0].get('date'),
        'other_news': other_news,
        'thumbnail': "/media/" + articol[0].get('file'),

    })


@staff_member_required
def news_preview(request):
    if request.method == "GET":
        return render(request, 'news/news.html', {
            'name': "{0}",
            'text': "{1}",
            'date': "{4}",
            'author': request.user.get_full_name(),
            'thumbnail': "{2}",
        })
    else:
        return HttpResponseForbidden()
