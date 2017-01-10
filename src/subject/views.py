from django.shortcuts import render
from django.http import HttpResponseForbidden
from django.contrib.auth.decorators import login_required

from forms import SubjectPostCreationForm


@login_required
def create_subject_post(request):
    if request.user.status != 2:
        raise HttpResponseForbidden
    form = SubjectPostCreationForm(request.POST or None)
    if form.is_valid():
        form.save()
    return render("subject/subject_post.html", {
        "form": form
    })
