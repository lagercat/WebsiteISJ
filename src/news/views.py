from django.shortcuts import render
from django.shortcuts import get_object_or_404
from django.http import Http404

from models import News


# Create your views here.

def news(request, slug):
    articol = get_object_or_404(News, slug=slug)
    other_news = News.objects.all()[:4]
    return render(request, 'news/news.html',
                  {
                      'news': articol,
                      'other_news': other_news,
                  })


def news_all(request):
    news = News.objects.all()
    return render(request, 'news/news_all.html', {
        'news_all': news,
    })
