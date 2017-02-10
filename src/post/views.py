from datetime import datetime, timedelta

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.utils.encoding import smart_str
from django.core.paginator import Paginator, EmptyPage
from django.http import HttpResponse, HttpResponseForbidden
from django.utils import timezone

from haystack.forms import SearchForm

from forms import CreatePostForm, FilterPostForm

from models import Post

import magic
from post.models import Page
from django.template import Template
from django.template.context import Context
from django.http.response import JsonResponse, HttpResponseRedirect
import json
from django.utils.safestring import mark_safe
from post.forms import PostFormSet
from django.contrib.admin.views.decorators import staff_member_required
from captcha.client import request

from django.db.models import Q

@login_required
def upload_file_form(request):
    form = CreatePostForm(request.POST or None, request.FILES or None, user=request.user)
    if request.method == 'POST':
        if form.is_valid():
            post = form.instance
            post.author = request.user
            post.save()
            return redirect("/files/1")
    return render(request, "post/form.html", {
        "form": form
    })


@login_required
def uploaded_files(request, page_id):
    form = SearchForm(request.GET or None)
    filters = FilterPostForm(request.POST or None)
    query = ""
    selects = [None] * 33
    if "q" in form.data and form.data['q'] and form.is_valid():
        results = form.search()
        query += "?q=" + form.data['q']
        files = [i.pk for i in results]
        files = Post.objects.filter(pk__in=files)
    else:
        files = Post.objects.all()
    if filters.is_valid():
        number_days = int(filters.cleaned_data['time'])
        permission = int(filters.cleaned_data['user_status'])
        selects[number_days] = "selected"
        selects[permission + 20] = "selected"
        if permission != -1:
            files = files.filter(author__status=permission)
        if number_days and files:
            target = datetime.now() - timedelta(days=number_days)
            target = timezone.make_aware(target, timezone.get_current_timezone())
            files = files.filter(date__gt=target)
    if files:
        files.latest('date')
        pages = Paginator(files, 10)
        try:
            files = pages.page(page_id)
        except EmptyPage:
            files = pages.page(pages.num_pages)
    return render(request, "post/posts.html", {
        "form": form,
        "selects": selects,
        "files": files,
        "query": query
    })


@login_required
def download_file(request, slug):
    post = get_object_or_404(Post, slug=slug)
    mime = magic.Magic(mime=True)
    response = HttpResponse(post.file, content_type=mime.from_file(post.file.path))
    response['Content-Disposition'] = 'attachment; filename=%s' % smart_str(post.filename)
    return response


@login_required
def delete_file(request, slug):
    post = get_object_or_404(Post, slug=slug)
    if post.author == request.user:
        post.delete()
        return redirect("/files/1")


@login_required
def edit_file(request, slug):
    post = get_object_or_404(Post, slug=slug)
    if post.author == request.user:
        form = CreatePostForm(request.POST or None, request.FILES or None, instance=post, user=request.user)
        if request.method == 'POST':
            if form.is_valid():
                form.save()
                return redirect("/files/1")
        return render(request, "post/edit.html", {
            "form": form
        })
    else:
        return HttpResponseForbidden()
      
def show_page(request, slug):
    page = get_object_or_404(Page, slug=slug)
    return HttpResponse("<head><title>" + page.name + '</title><link rel="stylesheet" type="text/css" href="/static/prism/prism.css"><script src="/static/prism/prism.js"></script></head><body>' + page.text + "</body>")


def files_filter(request):
    return JsonResponse({'results': list(Post.objects.filter(Q(name__contains=request.GET["query"]) |
                                                             Q(author__first_name__contains=request.GET["query"]) |
                                                             Q(author__last_name__contains=request.GET["query"]),
                                                            location="exterior")
                                                     .values('name', 'author__first_name', 'author__last_name', 'file'))})

@staff_member_required
def add_multiple_files(request):
    if request.method == "POST":
        visibility = request.POST["visibility"]
        request.POST.pop("visibility", None)
        print request.POST
        formset = PostFormSet(data=request.POST or None, files=request.FILES or None)
        print formset.is_valid()
        if formset.is_valid():
            instances = formset.save(commit=False)
            for instance in instances:
                instance.author = request.user
                instance.location = visibility;
                print instance
                instance.save()
            formset.save_m2m()
            return redirect("/admin/post/post/")
        else:
            response = HttpResponse(json.dumps({"errors" : formset.errors}), 
                content_type='application/json')
            response.status_code = 400
            return response
    else:
        return HttpResponseForbidden()

@staff_member_required      
def page_preview(request):
    if request.method == "GET":
        return HttpResponse("<head><title>" + "{0}" + '</title><link rel="stylesheet" type="text/css" href="/static/prism/prism.css"><script src="/static/prism/prism.js"></script></head><body>' + "{0}<br>" + request.user.get_full_name() + "<br>{1}" + "</body>")
    else:
        return HttpResponseForbidden()
    
  