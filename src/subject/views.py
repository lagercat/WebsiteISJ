from django.shortcuts import render
from django.http import HttpResponseForbidden
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404

from forms import SubjectPostCreationFormAdmin
from models import Subject, SubjectPost
from django.http.response import HttpResponse
from django.contrib.admin.views.decorators import staff_member_required


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
    materia = get_object_or_404(Subject, name=name)
    articole = SubjectPost.objects.all().filter(subject=materia)
    return render(request, 'subject/subject_all.html',
                  {
                      'articole': articole,
                      'materia': materia,
                  })


def subject_news(request, name, slug):
    articol = list(SubjectPost.objects.values('name', 'text', 'subject',
                                              'slug').filter(slug=slug,
                                                             subject__name=name))

    return render(request, 'subject/subject_news.html', {

        'name': articol[0].get('name'),
        'text': articol[0].get('text'),

    })

@staff_member_required   
def subject_news_preview(request):
    if request.method == "GET":
        return render(request, 'subject/subject_news.html', {

            'name': "{0}",
            'text': "{1}",
        })
    else:
        return HttpResponseForbidden()
