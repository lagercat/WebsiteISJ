'''
Created on Jan 13, 2017

@author: roadd
'''
from django import template
from post.models import Post
import json
from django.utils.safestring import mark_safe
from django.core import serializers

register = template.Library()

@register.assignment_tag
def get_files():
    return Post.objects.all()
