from django.shortcuts import render
from news.models import News
from event.models import Event


def home(request):
    if request.user.is_authenticated():
        template = 'homepages/home.html'
    else:
        template = 'homepages/index.html'
    noutati = News.objects.all()[:3]
    events = Event.objects.all()[:9]

    return render(request, template, {
        'noutati': noutati,
        'events': events,
    })
