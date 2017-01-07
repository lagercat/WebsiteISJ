from __future__ import unicode_literals
from authentication.models import ExtendedUser
from django.core.urlresolvers import reverse

from django.db import models


def upload_location(instance, filename):
    return "%s/%s" % (instance, filename)


# Create your models here.
class Event(models.Model):
    author = models.ForeignKey(ExtendedUser, related_name='event_post', blank='False')
    title = models.CharField(max_length=100, blank=False, null=True)
    description = models.CharField(max_length=5000, blank=False, null=True)
    location = models.CharField(max_length=100, blank=False, null=True)
    time = models.DateTimeField(null=True)
    image = models.ImageField(upload_to=upload_location, null=True, blank=True)

    def get_absolute_url(self):
        return reverse('event_post', args=[self.slug])
