from __future__ import unicode_literals

import uuid

from django.db import models
from django.core.urlresolvers import reverse


# Create your models here.
class Category(models.Model):
    title = models.CharField(max_length=20, blank=False, null=True)
    slug = models.SlugField(default=uuid.uuid1, unique=True,editable=False)

    def __unicode__(self):
        return self.title

    class Meta():
        get_latest_by = 'tile'
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'
        index_text = "Manage"


class Subcategory(models.Model):
    category = models.ForeignKey(Category, null=True)
    name = models.CharField(max_length=25, blank=False, null=True)
    slug_sub = models.SlugField(default=uuid.uuid1, unique=True,editable=False)

    def __unicode__(self):
        return self.name

    class Meta():
        get_latest_by = 'name'
        verbose_name = 'Subcategory'
        verbose_name_plural = 'Subcategories'
        index_text = "Manage"
