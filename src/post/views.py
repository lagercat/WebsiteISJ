from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from forms import CreatePostForm


@login_required
def upload_file_form(request):
    form = CreatePostForm(request.POST or None, request.FILES or None, user=request.user)
    confirm = []
    if request.method == 'POST':
        if form.is_valid():
            post = form.instance
            post.author = request.user
            post.save()
            confirm.append("Fisierul a fost incarcat")
    return render(request, "post/form.html", {
        "form": form,
        "confirm": confirm})

