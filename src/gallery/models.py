from __future__ import unicode_literals
from view_permission.models import CustomPermissionsMixin
from django.core.urlresolvers import reverse

from django.db import models
import os
import uuid


def user_directory_path(instance, filename):
    filename, file_extension = os.path.splitext(filename)
    return './documents/gallery/{0}/{1}{2}'.format(filename, instance.slug,
                                                   file_extension)


# Create your models here.
class Gallery(CustomPermissionsMixin):
    name = models.CharField(max_length=30, blank=False, null=True)
    description = models.CharField(max_length=1000, blank=False, null=True)
    date = models.DateTimeField(auto_now_add=True, editable=False, blank=True,
                                null=True)
    image = models.ImageField(upload_to=user_directory_path, null=True,
                              blank=False)
    slug = models.SlugField(default=uuid.uuid1, unique=True)

    def get_absolute_url(self):
        return reverse('news_post', args=[self.slug])
