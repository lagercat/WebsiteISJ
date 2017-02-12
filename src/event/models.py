from __future__ import unicode_literals
from authentication.models import ExtendedUser
from django.core.urlresolvers import reverse
from view_permission.models import CustomPermissionsMixin
from django.db import models
import os
import uuid
from post.models import File
from tinymce.models import HTMLField
from django.db.models.signals import pre_delete
from django.dispatch.dispatcher import receiver


def user_directory_path(instance, filename):
    filename, file_extension = os.path.splitext(filename)
    return './documents/events/{0}{1}'.format(instance.slug, file_extension)


# Create your models here.
class Event(File):
    def __init__(self, *args, **kwargs):
        self._meta.get_field('location').default = "thumbnails/events"
        self._meta.get_field('file').label = "Thumbnail"
        super(Event, self).__init__(*args, **kwargs)

    text = HTMLField()
    event_location = models.CharField(max_length=100, blank=False, null=True)

    REQUIRED = ['name', 'text', 'file', 'date', 'event_location']

    def __unicode__(self):
        return self.name

    class Meta(File.Meta):
        abstract = False
        verbose_name = "Event"
        verbose_name_plural = "Events"
        index_text = "Manage Events"
        
@receiver(pre_delete, sender=Event)
def file_delete(sender, instance, **kwargs):
    # Pass false so FileField doesn't save the model.
    instance.file.delete(False)
        