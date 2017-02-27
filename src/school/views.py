from django.shortcuts import render
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from models import School
from news.models import News
from config import settings



def schools_all(request):
    schools = School.objects.all()
    paginator = Paginator(schools, 4)

    page = request.GET.get('page')
    try:
        schools = paginator.page(page)
    except PageNotAnInteger:
        schools = paginator.page(1)
    except EmptyPage:
        schools = paginator.page(paginator.num_pages)
    return render(request, 'school/school_all.html', {
        'schools': schools,
    })


def schools(request, slug):
    articol = list(
        School.objects.values('name', 'telephone', 'fax', 'email', 'website',
                              'address',
                              'geolocation', 'file').filter(slug=slug))
    other_schools = School.objects.all()[:3]
    return render(request, 'school/school_detail.html', {
        'google_maps_api_key': settings.GOOGLE_MAPS_API_KEY,
        'name': articol[0].get('name'),
        'telephone': articol[0].get('telephone'),
        'fax': articol[0].get('fax'),
        'email': articol[0].get('email'),
        'website': articol[0].get('website'),
        'location': articol[0].get('address'),
        'geolocation': articol[0].get('geolocation'),
        'other_news': other_schools,
        'thumbnail': "/media/" + articol[0].get('file'),

    })
