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

from django.db import models
from django.db.models.signals import pre_delete
from django.dispatch.dispatcher import receiver

from post.models import File
from tinymce.models import HTMLField
from utility.models import CustomPermissionsMixin


def user_directory_path(self, filename):
    filename, file_extension = os.path.splitext(filename)
    return './documents/{0}/{1}{2}'.format(self.slug, file_extension,
                                           self.files_folder())


class Subject(CustomPermissionsMixin):
    class Meta(CustomPermissionsMixin.Meta):
        abstract = False
        verbose_name = "Subject"
        verbose_name_plural = "Subjects"
        index_text = "Create"

    name = models.CharField(max_length=60, null=True, unique=True)

    def __unicode__(self):
        return self.name

    def get_subject(self):
        subcategory_posts = Subcategory.objects.all().filter(subject=self)
        return subcategory_posts.get_subpost()

    def get_subcategory(self):
        subcategory = Subcategory.objects.all().filter(subject=self)
        return subcategory

    def get_subject_post(self):
        subject_post = SubjectPost.objects.all().filter(subject=self)
        return subject_post

    def get_simple_subject_post(self):
        subject_post = SubjectPost.objects.all().filter(subject=self, subcategory=None)
        return subject_post


class Subcategory(File):
    def __init__(self, *args, **kwargs):
        self._meta.get_field('location').default = "thumbnails/subjectpage"
        self._meta.get_field('file').label = "Thumbnail"
        super(Subcategory, self).__init__(*args, **kwargs)

    name = models.CharField(max_length=50, null=False, unique=True)
    subject = models.ForeignKey(Subject, blank=False, null=False)

    REQUIRED = ['subject', 'name', 'file']

    class Meta(File.Meta):
        abstract = False
        verbose_name = "Subcategory"
        verbose_name_plural = "Subcategories"
        index_text = "Manage"

    def __unicode__(self):
        return str(self.subject) + "/" + self.name

    def get_subpost(self):
        subpost = SubjectPost.objects.filter(subcategory=self).all()
        return subpost

    def get_name(self):
        return self.name

    def get_type(self):
        return type(self).__name__


class SubjectPost(File):
    def __init__(self, *args, **kwargs):
        self._meta.get_field('location').default = "thumbnails/subjectpage"
        self._meta.get_field('file').label = "Thumbnail"
        super(SubjectPost, self).__init__(*args, **kwargs)

    text = HTMLField()
    subcategory = models.ForeignKey(Subcategory, blank=True, null=True)
    subject = models.ForeignKey(Subject, blank=True, null=True)

    REQUIRED = ['subject', 'subcategory', 'name', 'text', 'file']

    def __unicode__(self):
        return self.name

    @property
    def get_type(self):
        return type(self).__name__

    class Meta(File.Meta):
        abstract = False
        verbose_name = "Subject Page"
        verbose_name_plural = "Subject Pages"
        index_text = "Manage"


@receiver(pre_delete, sender=Subcategory)
@receiver(pre_delete, sender=SubjectPost)
def file_delete(sender, instance, **kwargs):
    # Pass false so FileField doesn't save the model.
    instance.file.delete(False)
