from django.shortcuts import render
from django.shortcuts import get_object_or_404
from django.http import Http404

from models import News


# Create your views here.

def news(request, slug):
    articol = get_object_or_404(News, slug=slug)
    other_news = News.objects.all()[:4]
    return render(request, 'homepages/articol.html',
                  {
                      'news': articol,
                      'other_news': other_news,
                  })
