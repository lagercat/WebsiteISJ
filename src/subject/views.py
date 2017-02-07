from django.shortcuts import render
from django.http import HttpResponseForbidden
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404

from forms import SubjectPostCreationFormAdmin
from models import Subject, SubjectPost


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
                      'materia':materia,
                  })


def subject_news(request, name, slug):
    materia = get_object_or_404(Subject, name=name)
    articol = SubjectPost.objects.all().filter(subject=materia, slug=slug)
    return render(request, 'subject/subject_news', {
        'articol': articol,
    })
