from django.shortcuts import render
from django.http import HttpResponseForbidden
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404

from forms import SubjectPostCreationFormAdmin
from models import Subject, SubjectPost
from django.http.response import HttpResponse


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
    
def show_subject_page(request, slug):
    page = get_object_or_404(SubjectPost, slug=slug)
    return HttpResponse("<head><title>" + page.name + " " + page.subject + '</title><link rel="stylesheet" type="text/css" href="/static/prism/prism.css"><script src="/static/prism/prism.js"></script></head><body>' + page.text + "</body>")


