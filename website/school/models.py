from __future__ import unicode_literals

from django.db import models


class School(models.Model):
    name = models.CharField(max_length=100, default='')
