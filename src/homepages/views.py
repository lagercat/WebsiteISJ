from django.shortcuts import render, render_to_response
from news.models import News
from event.models import Event
from subject.models import Subject
from gallery.models import Gallery
from school.models import School
from page.models import Category, Subcategory
from django.template import RequestContext


def home(request):
    template = 'homepages/index.html'
    noutati = News.objects.all()[:3]
    events = Event.objects.all()[:9]
    subjects = Subject.objects.all()
    album = Gallery.objects.all()[:3]
    schools = School.objects.all()[:3]
    return render(request, template, {
        'noutati': noutati,
        'events': events,
        'subjects': subjects,
        'album': album,
        'schools':schools,
    })
