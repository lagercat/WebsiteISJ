# Copyright 2017 Adrian-Ioan Garovat, Emanuel Covaci, Sebastian-Valeriu Males
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
from django.dispatch.dispatcher import receiver
from django.template.defaultfilters import truncatechars
from django.utils.datetime_safe import datetime

from tinymce.models import HTMLField
from utility.models import CustomPermissionsMixin


def user_directory_path(self, filename):
    filename, file_extension = os.path.splitext(filename)
    return './documents/{0}/{1}{2}'.format(self.location,
                                           self.slug, file_extension)


class File(CustomPermissionsMixin):
    author = models.ForeignKey("authentication.ExtendedUser", blank=False)
    name = models.CharField(max_length=100, blank=False, null=True)
    file = models.FileField(upload_to=user_directory_path, null=True)
    date = models.DateTimeField(default=datetime.now, blank=False, null=True,
                                editable=True)
    slug = models.SlugField(default=uuid.uuid1, unique=True, editable=False)
    location = models.CharField(max_length=50, default="abstract")

    @property
    def filename(self):
        return os.path.basename(self.file.url)

    def fileLink(self):
        if self.file:
            return '<a href="' + "/download/" + str(self.slug) + '">'
            "Download file" + '</a>'
        else:
            return '<a href="''"></a>'

    fileLink.allow_tags = True
    fileLink.short_description = "Download"

    def __unicode__(self):
        return "File %s from %s" % (self.filename, self.author.username)

    @property
    def short_name(self):
        return truncatechars(self.name, 40)

    class Meta(CustomPermissionsMixin.Meta):
        abstract = True
        get_latest_by = 'date'
        verbose_name = 'File'
        verbose_name_plural = 'Files'

    @property
    def see_file(self):
        return self.file.url


class Post(File):

    def __init__(self, *args, **kwargs):
        self._meta.get_field('location').default = "interior"
        super(Post, self).__init__(*args, **kwargs)

    REQUIRED = ['name', 'file']

    class Meta(File.Meta):
        abstract = False
        get_latest_by = 'date'
        verbose_name = 'File'
        verbose_name_plural = 'Files'
        index_text = "Manage"


class Page(File):

    def __init__(self, *args, **kwargs):
        self._meta.get_field('location').default = "thumbails/pages"
        self._meta.get_field('file').label = "Thumbnail"
        super(Page, self).__init__(*args, **kwargs)

    text = HTMLField()

    REQUIRED = ['name', 'text', 'file']

    class Meta(Post.Meta):
        abstract = False
        get_latest_by = 'date'
        verbose_name = 'Page'
        verbose_name_plural = 'Pages'
        index_text = "Manage"


@receiver(pre_delete, sender=Page)
@receiver(pre_delete, sender=Post)
def file_delete(sender, instance, **kwargs):
    # Pass false so FileField doesn't save the model.
    instance.file.delete(False)
