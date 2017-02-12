from django.shortcuts import render
from django.shortcuts import get_object_or_404

from models import Event
from news.models import News
from django.contrib.admin.views.decorators import staff_member_required
from django.http.response import HttpResponseForbidden


# Create your views here.

def event_all(request):
    events = Event.objects.all()
    return render(request, 'event/events.html', {
        'events': events,
    })

def event_detail(request, slug):
    articol = list(Event.objects.values('name', 'text', 'date', 'file', 'author__first_name', 'author__last_name', 'event_location',
                                              'slug').filter(slug=slug))
    other_news = News.objects.all()[:4]
    return render(request, 'event/event_detail.html', {

        'name': articol[0].get('name'),
        'text': articol[0].get('text'),
        'event_location': articol[0].get('event_location'),
        'author': articol[0].get('author__first_name') + " " + articol[0].get('author__last_name'),
        'date': articol[0].get('date'),
        'other_news': other_news,
        'thumbnail': "/media/" + articol[0].get('file'),

    })
    
@staff_member_required   
def event_detail_preview(request):
    if request.method == "GET":
        return render(request, 'event/event_detail.html', {
            'name': "{0}",
            'text': "{1}",
            'author': request.user.get_full_name(),
            'event_location': "{3}",
            'date': "{4}",
            'thumbnail': "{2}",
        })
    else:
        return HttpResponseForbidden()