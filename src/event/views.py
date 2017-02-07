from django.shortcuts import render
from django.shortcuts import get_object_or_404

from models import Event


# Create your views here.

def event(request, slug):
    event = get_object_or_404(Event, slug=slug)
    other_event = Event.object.all()[:4]
    return render(request, 'event/event_detail.html', {
        'event': event,
        'other_event': event,
    })


def event_all(request):
    events = Event.object.all()
    return render(request, 'event/events.html', {
        'events': events,
    })
