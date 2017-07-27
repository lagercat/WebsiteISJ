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

from django.db import models
from django.db.models.fields.related import ForeignKey
from django.db.models.signals import pre_delete
from django.dispatch.dispatcher import receiver

from post.models import File
from utility.models import CustomPermissionsMixin


class Gallery(File):
    def __init__(self, *args, **kwargs):
        self._meta.get_field('location').default = "gallery/thumbnails"
        super(Gallery, self).__init__(*args, **kwargs)

    REQUIRED = ['name', 'file']

    class Meta(File.Meta):
        verbose_name = "Gallery"
        verbose_name_plural = "Galleries"
        index_text = "Manage"


class GalleryPhoto(File):
    def __init__(self, *args, **kwargs):
        self._meta.get_field('location').default = "gallery/placeholder"
        super(GalleryPhoto, self).__init__(*args, **kwargs)

    gallery = ForeignKey(Gallery, null=False, blank=False, on_delete=models.CASCADE)

    REQUIRED = ['gallery', 'name', 'file']

    def __unicode__(self):
        return self.name

    class Meta(File.Meta):
        abstract = False
        verbose_name = "Gallery Photo"
        verbose_name_plural = "Gallery Photos"
        index_text = "Manage"


@receiver(pre_delete, sender=Gallery)
@receiver(pre_delete, sender=GalleryPhoto)
def file_delete(sender, instance, **kwargs):
    # Pass false so FileField doesn't save the model.
    instance.file.delete(False)
