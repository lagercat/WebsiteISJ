from django.shortcuts import render
from django.http import HttpResponseForbidden
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404

from forms import SubjectPostCreationFormAdmin
from models import Subject, SubjectPost
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
    return render(request, 'subject/subject_all.html',
                  {

                      'materia': subject.get_subcategory(),
                      'simples':subject.get_subject_post(),

                  })


def subject_news(request, name, slug):
    articol = list(SubjectPost.objects.values('name', 'text', 'subject', 'file',
                                              'slug').filter(slug=slug,
                                                             subject__name=name))
    other_news = News.objects.all()[:4]
    return render(request, 'subject/subject_news.html', {

        'name': articol[0].get('name'),
        'text': articol[0].get('text'),
        'other_news': other_news,
        'thumbnail': "/media/" + articol[0].get('file'),

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
