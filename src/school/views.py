from config import settings

from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.shortcuts import render

from models import School


def schools_all(request):
    all_schools = School.objects.all()
    paginator = Paginator(all_schools, 4)

    page = request.GET.get('page')
    try:
        all_schools = paginator.page(page)
    except PageNotAnInteger:
        all_schools = paginator.page(1)
    except EmptyPage:
        all_schools = paginator.page(paginator.num_pages)
    return render(request, 'school/school_all.html', {
        'schools': all_schools,
    })


def schools_map(request):
    school = School.objects.all().order_by('name')
    return render(request, 'school/school_map.html', {
        'google_maps_api_key': settings.GOOGLE_MAPS_API_KEY,
        'schools': school,
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
