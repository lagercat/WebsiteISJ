from django.shortcuts import render


from models import School


# Create your views here.

def school_all(request):
    school = School.objects.all()
    return render(request, 'school/school_all.html', {
        'news_all': school,
    })