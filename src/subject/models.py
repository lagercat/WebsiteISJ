from __future__ import unicode_literals
import os

from django.db import models
from post.models import Post


def user_directory_path(self, filename):
    filename, file_extension = os.path.splitext(filename)
    return './documents/{0}/{1}{2}'.format(self.slug, file_extension,
                                           self.files_folder())


class Subject(models.Model):
    class Meta:
        verbose_name = "subject"
        verbose_name_plural = "subjects"

    name = models.CharField(max_length=50, null=True, unique=True)

    def __unicode__(self):
        return self.name


class SubjectPost(Post):
    @staticmethod
    def files_folder():
        return "interior"

    text = models.TextField()
    subject = models.ForeignKey(Subject, blank=False, null=False)

    REQUIRED = ['subject', 'name', 'text', 'file']

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name = "post"
        verbose_name_plural = "posts"
