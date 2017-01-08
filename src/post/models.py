from __future__ import unicode_literals
import os
import uuid

from authentication.models import ExtendedUser
from django.db import models
from view_permission.models import CustomPermissionsMixin


def user_directory_path(instance, filename):
    filename, file_extension = os.path.splitext(filename)
    return './documents/{0}{1}'.format(instance.slug, file_extension)


class Post(CustomPermissionsMixin):
    author = models.ForeignKey(ExtendedUser, blank=False)
    author_status = models.IntegerField(default=-1)
    name = models.CharField(max_length=100, blank=False, null=True)
    file = models.FileField(upload_to=user_directory_path)
    date = models.DateTimeField(auto_now_add=True, editable=False, blank=False, null=True)
    slug = models.SlugField(default=uuid.uuid1, unique=True)

    @property
    def filename(self):
        return os.path.basename(self.file.url)

    def fileLink(self):
      if self.file:
          return '<a href="' + str(self.file.url) + '">' + "See file" + '</a>'
      else:
          return '<a href="''"></a>'
    fileLink.allow_tags = True
    fileLink.short_description = "File Link"

    def __unicode__(self):
        return "File %s from %s" % (self.filename, self.author.username)

    class Meta(CustomPermissionsMixin.Meta):
        abstract = False
        get_latest_by = 'date'
        verbose_name = 'File'
        verbose_name_plural = 'Files'
