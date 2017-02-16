from __future__ import unicode_literals

from django.db import models


class School(models.Model):
    name = models.CharField(max_length=100, null=True)

    def __unicode__(self):
        return self.name

    class Meta():
        verbose_name = "School"
        verbose_name_plural = "Schools"
        index_text = "Manage"