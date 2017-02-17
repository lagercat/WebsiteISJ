from __future__ import unicode_literals

import uuid

from django.db import models
from django.core.urlresolvers import reverse


# Create your models here.
class Header_tile(models.Model):
    title = models.CharField(max_length=20, blank=False, null=True)
    slug = models.SlugField(default=uuid.uuid1, unique=True,editable=False)


class Subcategory_heder_tile(models.Model):
    Header_tile = models.ForeignKey(Header_tile, null=True)
    name = models.CharField(max_length=25, blank=False, null=True)
    slug_sub = models.SlugField(default=uuid.uuid1, unique=True,editable=False)
