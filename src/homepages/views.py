from django.shortcuts import render
from news.models import News
from event.models import Event
from subject.models import Subject
from page.models import Category, Subcategory
from django.template import RequestContext


def home(request):
    template = 'homepages/index.html'
    noutati = News.objects.all()[:3]
    events = Event.objects.all()[:9]
    subjects = Subject.objects.all()
    return render(request, template, {
        'noutati': noutati,
        'events': events,
        'subjects':subjects,
    },
     context_instance=RequestContext(request))

