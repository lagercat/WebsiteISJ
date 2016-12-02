from __future__ import unicode_literals
import os

from django.db import models
from django.contrib.auth.models import User


class Post(models.Model):
    author = models.ForeignKey(User, related_name='posts', blank=False)
    file = models.FileField()
    date = models.DateTimeField(Editable=False, auto_now_add=True, blank=False)

    @property
    def filename(self):
        return os.path.basename(self.file)

    def __unicode__(self):
        return "File %s from %s" % (self.filename, self.author.username)

    class Meta:
        get_latest_by = 'date'
