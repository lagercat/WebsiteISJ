from django.shortcuts import render
from django.shortcuts import get_object_or_404
from django.http import Http404

from models import News
from django.contrib.admin.views.decorators import staff_member_required
from django.http.response import HttpResponseForbidden


# Create your views here.

def news_all(request):
    news = News.objects.all()
    return render(request, 'news/news_all.html', {
        'news_all': news,
    })


def news(request, slug):
    articol = list(News.objects.values('name', 'text', 'author__first_name', 'author__last_name', 'file', 'date'
                                              'slug').filter(slug=slug))
    other_news = News.objects.all()[:4]
    return render(request, 'news/news.html', {

        'name': articol[0].get('name'),
        'text': articol[0].get('text'),
        'author': articol[0].get('author__first_name') + " " + articol[0].get('author__last_name'),
        'date': articol[0].get('date'),
        'other_news': other_news,
        'thumbnail': "/media/" + articol[0].get('file'),

    })

@staff_member_required   
def news_preview(request):
    if request.method == "GET":
        return render(request, 'news/news.html', {
            'name': "{0}",
            'text': "{1}",
            'date': "{4}",
            'author': request.user.get_full_name(),
            'thumbnail': "{2}",
        })
    else:
        return HttpResponseForbidden()
          
