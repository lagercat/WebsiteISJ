from __future__ import unicode_literals

import os

from django.db.models.signals import pre_delete
from django.dispatch.dispatcher import receiver

from authentication.models import ExtendedUser
from django_google_maps import fields as map_fields
from post.models import File
from tinymce.models import HTMLField
from utility.models import CustomPermissionsMixin


def user_directory_path(instance, filename):
    filename, file_extension = os.path.splitext(filename)
    return './documents/events/{0}{1}'.format(instance.slug, file_extension)


class Event(File):
    def __init__(self, *args, **kwargs):
        self._meta.get_field('location').default = "thumbnails/events"
        self._meta.get_field('file').label = "Thumbnail"
        super(Event, self).__init__(*args, **kwargs)

    text = HTMLField()
    address = map_fields.AddressField(max_length=200)
    geolocation = map_fields.GeoLocationField(max_length=100)

    REQUIRED = ['name', 'text', 'file', 'date', 'address', 'geolocation']

    def __unicode__(self):
        return self.name

    class Meta(File.Meta):
        abstract = False
        verbose_name = "Event"
        verbose_name_plural = "Events"
        index_text = "Manage"


@receiver(pre_delete, sender=Event)
def file_delete(sender, instance, **kwargs):
    # Pass false so FileField doesn't save the model.
    instance.file.delete(False)
