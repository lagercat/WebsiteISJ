from __future__ import unicode_literals
import os

from django.db import models
from django.contrib.auth.models import User


class Post(models.Model):
    author = models.ForeignKey(User, related_name='posts', blank=False)
    name = models.CharField(max_length=100, blank=False, null=True)
    file = models.FileField()
    date = models.DateTimeField(editable=False, auto_now_add=True, blank=False, null=True)

    @property
    def filename(self):
        return os.path.basename(self.file)

    def __unicode__(self):
        return "File %s from %s" % (self.filename, self.author.username)

    class Meta:
        get_latest_by = 'date'
