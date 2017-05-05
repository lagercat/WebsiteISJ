from itertools import chain

from django.shortcuts import render
from django.http import HttpResponseForbidden
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from forms import SubjectPostCreationFormAdmin
from models import Subject, SubjectPost, Subcategory
from django.http.response import HttpResponse
from django.contrib.admin.views.decorators import staff_member_required
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
    subject = get_object_or_404(Subject, name=name)
    results = sorted(list(
        chain(subject.get_subcategory(), subject.get_subject_post())),
        key=lambda instance: instance.date, reverse=True)
    paginator = Paginator(results, 4)

    page = request.GET.get('page')
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)
    return render(request, 'subject/subject_all.html',
                  {
                      'name':name,
                      'posts': posts
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
    return render(request, 'subject/subcategory_post.html',
                  {
                      'subcategory_article': posts,
                      'name':name,
                      'kind':kind
                  })


def subcategory_subject_news(request,name,kind,slug):
    articol = list(
        SubjectPost.objects.values('name', 'text', 'subject', 'file',
                                   'slug').filter(slug=slug,
                                                  subcategory__name=kind))
    other_news = News.objects.all()[:4]
    return render(request, 'subject/subject_news.html', {


        'name': articol[0].get('name'),
        'text': articol[0].get('text'),
        'other_news': other_news,
        'thumbnail': "/media/" + articol[0].get('file'),
        'name_subject':name,


    })


def subject_news(request, name, slug):
    articol = list(
        SubjectPost.objects.values('name', 'text', 'subject', 'file',
                                   'slug').filter(slug=slug,
                                                  subject__name=name))
    other_news = News.objects.all()[:4]
    return render(request, 'subject/subject_news.html', {

        'name': articol[0].get('name'),
        'text': articol[0].get('text'),
        'other_news': other_news,
        'thumbnail': "/media/" + articol[0].get('file'),

    })

def subject_page_all(request):
    subjects = Subject.objects.all()
    return render(request,'subject/specializari.html',{
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
