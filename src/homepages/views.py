from django.shortcuts import render, render_to_response
from django.template import RequestContext

from event.models import Event
from gallery.models import Gallery
from news.models import News
from page.models import Category, Subcategory
from school.models import School
from subject.models import Subject


def home(request):
    template = 'homepages/index.html'
    noutati = News.objects.all()[:3]
    events = Event.objects.all()[:9]
    subjects = Subject.objects.all()[:6]
    album = Gallery.objects.all()[:3]
    schools = School.objects.all()[:3]
    return render(request, template, {
        'noutati': noutati,
        'events': events,
        'subjects': subjects,
        'album': album,
        'schools':schools,
    })
