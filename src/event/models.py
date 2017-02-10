from __future__ import unicode_literals
from authentication.models import ExtendedUser
from django.core.urlresolvers import reverse
from view_permission.models import CustomPermissionsMixin
from django.db import models
import os
import uuid


def user_directory_path(instance, filename):
    filename, file_extension = os.path.splitext(filename)
    return './documents/events/{0}{1}'.format(instance.slug, file_extension)


# Create your models here.
class Event(CustomPermissionsMixin):
    author = models.ForeignKey(ExtendedUser, related_name='event_post',
                               blank='False')
    title = models.CharField(max_length=100, blank=False, null=True)
    description = models.CharField(max_length=5000, blank=False, null=True)
    location = models.CharField(max_length=100, blank=False, null=True)
    time = models.DateTimeField(null=True)
    image = models.ImageField(upload_to=user_directory_path, null=True,
                              blank=True)
    slug = models.SlugField(default=uuid.uuid1, unique=True, editable=False)

    def __unicode__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('event_post', args=[self.slug])

    class Meta(CustomPermissionsMixin.Meta):
        abstract = False
        get_latest_by = 'time'
        verbose_name = 'Event'
        verbose_name_plural = 'Events'
