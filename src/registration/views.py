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


def pre_school(request):
    documents_all = list(Registration.objects.filter(
        type_registration=2
    ))
    return render(request, 'registration/primary_all.html', {
        'documents_all': documents_all,
        'title':'Invatamant prescolar'
    })
