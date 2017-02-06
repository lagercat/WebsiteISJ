from django.shortcuts import render
from news.models import News


def home(request):
    if request.user.is_authenticated():
        template = 'homepages/home.html'
    else:
        template = 'homepages/index.html'
    noutati = News.objects.all()
    return render(request, template,{
        'noutati':noutati,
    })
