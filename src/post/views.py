from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404
from django.utils.encoding import smart_str
from django.http import HttpResponse

from forms import CreatePostForm
from models import Post

import magic


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


@login_required
def uploaded_files(request):
    files = Post.objects.all().order_by('-date')
    return render(request, "post/posts.html", {
        "files": files
    })


@login_required
def download_file(request, slug):
    post = get_object_or_404(Post, slug=slug)
    mime = magic.Magic(mime=True)
    response = HttpResponse(post.file, content_type=mime.from_file(post.file.path))
    response['Content-Disposition'] = 'attachment; filename=%s' % smart_str(post.filename)
    return response

