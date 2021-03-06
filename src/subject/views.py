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
from itertools import chain

from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import login_required
from django.core.paginator import EmptyPage
from django.core.paginator import PageNotAnInteger
from django.core.paginator import Paginator
from django.http import HttpResponseForbidden
from django.shortcuts import get_object_or_404
from django.shortcuts import render

from forms import SubjectPostCreationFormAdmin
from models import Subcategory
from models import Subject
from models import SubjectPost
from news.models import News


@login_required
def create_subject_post(request):
    if request.user.status != 2:
        return HttpResponseForbidden()
    form = SubjectPostCreationFormAdmin(request.POST or None,
                                        request.FILES or None,
                                        user=request.user)
    if request.method == "POST":
        if form.is_valid():
            form.save()
    return render(request, "subject/subject_post.html", {
        "form": form
    })


def subject(request, name):
    current_subject = get_object_or_404(Subject, name=name)
    results = sorted(list(
        chain(current_subject.get_subcategory(),
              current_subject.get_simple_subject_post())),
        key=lambda instance: instance.date, reverse=True)
    paginator = Paginator(results, 4)

    page = request.GET.get('page')
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)

    index = posts.number - 1
    max_index = len(paginator.page_range)
    start_index = index - 3 if index >= 3 else 0
    end_index = index + 3 if index <= max_index - 3 else max_index
    page_range = list(paginator.page_range)[start_index:end_index]

    return render(request, 'subject/subject_all.html',
                  {
                      'name': name,
                      'posts': posts,
                      'page_range': page_range
                  })


def subcategory_subject(request, name, kind):
    sub = get_object_or_404(Subcategory, name=kind)
    posts = sub.get_subpost()
    paginator = Paginator(posts, 4)

    page = request.GET.get('page')
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)

    index = posts.number - 1
    max_index = len(paginator.page_range)
    start_index = index - 3 if index >= 3 else 0
    end_index = index + 3 if index <= max_index - 3 else max_index
    page_range = list(paginator.page_range)[start_index:end_index]

    return render(request, 'subject/subcategory_post.html',
                  {
                      'subcategory_article': posts,
                      'name': name,
                      'kind': kind,
                      'page_range': page_range
                  })


def subcategory_subject_news(request, name, kind, slug):
    articol = list(
        SubjectPost.objects.values('name', 'text', 'subject', 'file',
                                   'slug', 'date').filter(
            slug=slug,
            subcategory__name=kind))
    other_news = News.objects.all()[:4]
    return render(request, 'subject/subject_news.html', {

        'name': articol[0].get('name'),
        'text': articol[0].get('text'),
        'date': articol[0].get('date'),
        'other_news': other_news,
        'thumbnail': "/media/" + articol[0].get('file'),
        'subject_name': name,
        'subcategory': kind,

    })


def subject_news(request, name, slug):
    articol = list(
        SubjectPost.objects.values('name', 'text', 'subject', 'file',
                                   'slug', 'date').filter(
            slug=slug,
            subject__name=name))
    other_news = News.objects.all()[:4]
    return render(request, 'subject/subject_news.html', {

        'name': articol[0].get('name'),
        'subject_name': name,
        'date': articol[0].get('date'),
        'text': articol[0].get('text'),
        'other_news': other_news,
        'thumbnail': "/media/" + articol[0].get('file'),

    })


def subject_page_all(request):
    subjects = Subject.objects.all()
    return render(request, 'subject/specializari.html', {
        'subjects': subjects,
    })


@staff_member_required
def subject_news_preview(request):
    if request.method == "GET":
        return render(request, 'subject/subject_news.html', {
            'name': "{0}",
            'text': "{1}",
            'thumbnail': "{2}",
        })
    else:
        return HttpResponseForbidden()
