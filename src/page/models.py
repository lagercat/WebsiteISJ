# Copyright 2017 Adrian-Ioan Gărovăț, Emanuel Covaci, Sebastian-Valeriu Maleș
#
# This file is part of WebsiteISJ
#
# WebsiteISJ is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# WebsiteISJ is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with WebsiteISJ.   If not, see <http://www.gnu.org/licenses/>.
from __future__ import unicode_literals

import os
import uuid

from django.db import models
from django.db.models.signals import pre_delete
from django.dispatch import receiver

from post.models import File
from tinymce.models import HTMLField
from utility.models import CustomPermissionsMixin


def user_directory_path(instance, filename):
    filename, file_extension = os.path.splitext(filename)
    return './documents/category/{0}{1}'.format(instance.slug, file_extension)


class Category(CustomPermissionsMixin):
    class Meta(CustomPermissionsMixin.Meta):
        get_latest_by = 'title'
        abstract = False
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'
        index_text = "Manage"
        
    title = models.CharField(max_length=20, blank=False, null=True,
                             unique=True)
    slug = models.SlugField(default=uuid.uuid1, unique=True, editable=False)

    @property
    def url_link(self):
        return "/category/" + self.slug

    def __unicode__(self):
        return self.title


class Subcategory(CustomPermissionsMixin):
    category = models.ForeignKey(Category, related_name='subcategories',
                                 null=True)
    name = models.CharField(max_length=25, blank=False, null=True, unique=True)
    slug_sub = models.SlugField(default=uuid.uuid1, unique=True,
                                editable=False)

    def __unicode__(self):
        return self.name

    class Meta(CustomPermissionsMixin.Meta):
        get_latest_by = 'title'
        abstract = False
        verbose_name = 'Subcategory'
        verbose_name_plural = 'Subcategories'
        index_text = "Manage"

    @property
    def url_link(self):
        return "/subcategory/" + self.slug_sub


class Article(File):
    def __init__(self, *args, **kwargs):
        self._meta.get_field('location').default = "thumbnails/Article"
        self._meta.get_field('file').label = "Thumbnail"
        super(Article, self).__init__(*args, **kwargs)

    text = HTMLField()
    subcategory = models.ForeignKey(Subcategory, blank=False, null=False)

    REQUIRED = ['subcategory', 'name', 'text', 'file']  # 'category'

    def __unicode__(self):
        return self.name

    class Meta(File.Meta):
        abstract = False
        verbose_name = "Article"
        verbose_name_plural = "Articles"
        index_text = "Manage"

    @property
    def url_link(self):
        return "/article/" + self.slug


class SimplePage(File):
    def __init__(self, *args, **kwargs):
        self._meta.get_field('location').default = "thumbnails/Article"
        self._meta.get_field('file').label = "Thumbnail"
        super(SimplePage, self).__init__(*args, **kwargs)

    text = HTMLField()
    category = models.ForeignKey(Category, related_name='simplepages',
                                 blank=False, null=False)

    REQUIRED = ['category', 'name', 'text', 'file']

    def __unicode__(self):
        return self.name

    class Meta(File.Meta):
        abstract = False
        verbose_name = "Simple page"
        verbose_name_plural = "Simple pages"
        index_text = "Manage"

    @property
    def url_link(self):
        return "/simple/" + self.slug


@receiver(pre_delete, sender=SimplePage)
@receiver(pre_delete, sender=Article)
def file_delete(sender, instance, **kwargs):
    # Pass false so FileField doesn't save the model.
    instance.file.delete(False)
