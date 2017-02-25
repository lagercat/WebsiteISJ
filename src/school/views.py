from django.shortcuts import render

from models import School
from news.models import News
from config import settings


# Create your views here.

def schools_all(request):
    school = School.objects.all()
    return render(request, 'school/school_all.html', {
        'news_all': school,
    })


def schools(request, slug):
    print "Am ajuns aici"
    articol = list(
        School.objects.values('name', 'telephone', 'fax', 'email', 'website',
                              'address',
                              'geolocation', 'file').filter(slug=slug))
    other_news = School.objects.all()[:4]
    return render(request, 'school/school_detail.html', {
        'google_maps_api_key': settings.GOOGLE_MAPS_API_KEY,
        'name': articol[0].get('name'),
        'telephone': articol[0].get('telephone'),
        'fax': articol[0].get('fax'),
        'email': articol[0].get('email'),
        'website': articol[0].get('website'),
        'location': articol[0].get('address'),
        'geolocation': articol[0].get('geolocation'),
        'other_news': other_news,
        'thumbnail': "/media/" + articol[0].get('file'),

    })
