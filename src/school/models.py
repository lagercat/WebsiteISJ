from __future__ import unicode_literals

from django.db import models
from utility.models import CustomPermissionsMixin


class School(CustomPermissionsMixin):
    class Meta(CustomPermissionsMixin.Meta):
        abstract = False
        verbose_name = "School"
        verbose_name_plural = "Schools"
        index_text = "Manage"
    name = models.CharField(max_length=100, null=True)

    def __unicode__(self):
        return self.name
