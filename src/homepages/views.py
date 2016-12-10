from django.shortcuts import render


def home(request):
    if request.user.is_authenticated():
        template = 'homepages/home.html'
    else:
        template = 'homepages/index.html'
    return render(request, template)
