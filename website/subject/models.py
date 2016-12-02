from __future__ import unicode_literals

from django.db import models


class Subject(models.Model):
    name = models.CharField(max_length=50, null=True)

    def __unicode__(self):
        return  self.name