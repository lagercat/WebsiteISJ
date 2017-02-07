from django.shortcuts import render
from news.models import News
from event.models import Event
from subject.models import Subject


def home(request):
    if request.user.is_authenticated():
        template = 'homepages/home.html'
    else:
        template = 'homepages/index.html'
    noutati = News.objects.all()[:3]
    events = Event.objects.all()[:9]
    subjects = Subject.objects.all()

    return render(request, template, {
        'noutati': noutati,
        'events': events,
        'subjects': subjects,
    })
