from __future__ import unicode_literals

import os
import uuid

from django.db import models
from django.db.models.signals import pre_delete
from django.dispatch.dispatcher import receiver

from django_google_maps import fields as map_fields
from post.models import File
from utility.models import CustomPermissionsMixin


def user_directory_path(instance, filename):
    filename, file_extension = os.path.splitext(filename)
    return './documents/school/{0}{1}'.format(instance.slug, file_extension)


class School(CustomPermissionsMixin):
    class Meta(CustomPermissionsMixin.Meta):
        abstract = False
        verbose_name = "School"
        verbose_name_plural = "Schools"
        index_text = "Manage"

    name = models.CharField(max_length=100, null=True)
    telephone = models.CharField(max_length=11, blank=True)
    fax = models.CharField(max_length=15, blank=True)
    email = models.EmailField(max_length=20, blank=True)
    website = models.CharField(max_length=100, blank=True)
    address = map_fields.AddressField(max_length=200)
    geolocation = map_fields.GeoLocationField(max_length=100)
    file = models.FileField(upload_to=user_directory_path, null=True)
    slug = models.SlugField(default=uuid.uuid1, unique=True, editable=False)
    location = models.CharField(max_length=50, default="thumbnails/school")

    REQUIRED = ['name', 'address', 'geolocation']

    def __unicode__(self):
        return self.name


@receiver(pre_delete, sender=School)
def file_delete(sender, instance, **kwargs):
    # Pass false so FileField doesn't save the model.
    instance.file.delete(False)
