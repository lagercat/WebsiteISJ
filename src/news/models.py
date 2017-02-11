from __future__ import unicode_literals
from authentication.models import ExtendedUser
from view_permission.models import CustomPermissionsMixin
from django.db import models
from django.core.urlresolvers import reverse

import os
import uuid


# Create your models here.

def user_directory_path(instance, filename):
    filename, file_extension = os.path.splitext(filename)
    return './documents/news/{0}{1}'.format(instance.slug, file_extension)


class News(CustomPermissionsMixin):
    author = models.ForeignKey(ExtendedUser, related_name='news', blank=False)
    title = models.CharField(max_length=100, blank=False, null=True)
    description = models.CharField(max_length=5000, blank=False, null=True)
    image = models.ImageField(upload_to=user_directory_path, null=True,
                              blank=False)
    date_creation = models.DateTimeField(null=True)
    slug = models.SlugField(default=uuid.uuid1, unique=True, editable=False)

    def __unicode__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('news_post', args=[self.slug])

    class Meta(CustomPermissionsMixin.Meta):
        abstract = False
        verbose_name = 'News'
        verbose_name_plural = 'News'
        index_text = "Manage News"
