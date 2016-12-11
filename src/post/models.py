from __future__ import unicode_literals
import os
import uuid

from django.contrib.auth.models import User
from django.db import models


def user_directory_path(instance, filename):
    return 'documents/user_{0}/{1}'.format(instance.author.username, filename)


class Post(models.Model):
    author = models.ForeignKey(User, related_name='posts', blank=False)
    name = models.CharField(max_length=100, blank=False, null=True)
    file = models.FileField(upload_to=user_directory_path)
    date = models.DateTimeField(editable=False, auto_now_add=True, blank=False, null=True)
    slug = models.SlugField(default=uuid.uuid1, unique=True)

    @property
    def filename(self):
        return os.path.basename(self.file.url)

    def __unicode__(self):
        return "File %s from %s" % (self.filename, self.author.username)

    class Meta:
        get_latest_by = 'date'
