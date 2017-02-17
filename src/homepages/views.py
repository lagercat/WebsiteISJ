from django.shortcuts import render
from news.models import News
from event.models import Event
from subject.models import Subject
from page.models import Category,Subcategory


def home(request):
    template = 'homepages/index.html'
    noutati = News.objects.all()[:3]
    events = Event.objects.all()[:9]
    subjects = Subject.objects.all()
    category = Category.objects.all()
    subcategory = Subcategory.objects.all()
    header = {
        value.title: list(Subcategory.objects.all().filter(category=value).order_by("name").values("name",)) for value in category
    }
    print header
    return render(request, template, {
        'header': header.items(),
        'noutati': noutati,
        'events': events,
        'subjects': subjects,
    })
