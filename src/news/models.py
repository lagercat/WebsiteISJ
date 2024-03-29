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

from django.db.models.signals import pre_delete
from django.dispatch.dispatcher import receiver

from post.models import File
from tinymce.models import HTMLField


def user_directory_path(instance, filename):
    filename, file_extension = os.path.splitext(filename)
    return './documents/news/{0}{1}'.format(instance.slug, file_extension)


class News(File):
    def __init__(self, *args, **kwargs):
        self._meta.get_field('location').default = "thumbnails/news"
        self._meta.get_field('file').label = "Thumbnail"
        super(News, self).__init__(*args, **kwargs)

    text = HTMLField()

    REQUIRED = ['name', 'text', 'file']

    def __unicode__(self):
        return self.name

    class Meta(File.Meta):
        abstract = False
        verbose_name = "News"
        verbose_name_plural = "News"
        index_text = "Manage"

    @property
    def url_link(self):
        return "/news/"+self.slug


@receiver(pre_delete, sender=News)
def file_delete(sender, instance, **kwargs):
    # Pass false so FileField doesn't save the model.
    instance.file.delete(False)
