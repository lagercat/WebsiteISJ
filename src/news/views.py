from django.shortcuts import render
from django.shortcuts import get_object_or_404
from django.http import Http404

from models import News


# Create your views here.

def news(request, slug):
    articol = get_object_or_404(News, slug=slug)
    return render(request, 'homepages/articol.html',
                  {
                      'news': articol,
                  })
