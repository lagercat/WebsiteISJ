from django.shortcuts import render
from models import Gallery


# Create your views here.

def gallery(request):
    image = Gallery.objects.all()
    return render(request, 'gallery/gallery.html', {
        'gallery': image,
    })
