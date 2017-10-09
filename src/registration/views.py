# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render

# Create your views here.
def primary_school(request):
    return render(request,'registration/primary_all.html')

def pre_school(request):
    return render(request,'registration/pre-school_all.html')