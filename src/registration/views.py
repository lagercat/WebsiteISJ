# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from .models import Registration


# Create your views here.
def primary_school(request):
    documents_all = list(Registration.objects.filter(
        type_registration=1
    ))
    return render(request, 'registration/primary_all.html', {
        'documents_all': documents_all,
        'title':'Invatamant primar'
    })

def school_registration_detail(request,slug):
    detail = list(Registration.objects.values('name', 'text', 'author__first_name',
                                       'author__last_name', 'file',
                                       'slug').filter(slug=slug))
    return render(request, 'registration/registration_detail.html', {

        'name': detail[0].get('name'),
        'text': detail[0].get('text'),
        'author': detail[0].get(
            'author__first_name') + " " + detail[0].get('author__last_name'),
        'date': detail[0].get('date'),
        'thumbnail': "/media/" + detail[0].get('file'),

    })



def pre_school(request):
    documents_all = list(Registration.objects.filter(
        type_registration=2
    ))
    return render(request, 'registration/primary_all.html', {
        'documents_all': documents_all,
        'title':'Invatamant prescolar'
    })
