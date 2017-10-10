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

from django_google_maps import fields as map_fields
from phonenumber_field.modelfields import PhoneNumberField

from utility.models import CustomPermissionsMixin


def user_directory_path(instance, filename):
    filename, file_extension = os.path.splitext(filename)
    return './documents/school/{0}{1}'.format(instance.slug, file_extension)


class School(CustomPermissionsMixin):
    class Meta(CustomPermissionsMixin.Meta):
        abstract = False
        verbose_name = "School"
        verbose_name_plural = "Schools"
        index_text = "Manage"

    name = models.CharField(max_length=100, null=True)
    telephone = PhoneNumberField(blank=True)
    fax = PhoneNumberField(blank=True)
    email = models.EmailField(max_length=20, blank=True)
    website = models.CharField(max_length=100, blank=True)
    address = map_fields.AddressField(max_length=200)
    geolocation = map_fields.GeoLocationField(max_length=100)
    file = models.FileField(upload_to=user_directory_path, null=True,
                            blank=True)
    slug = models.SlugField(default=uuid.uuid1, unique=True, editable=False)
    location = models.CharField(max_length=50, default="thumbnails/school")
    STATUS_CHOICES = (
        (0, "Gradinita"),
        (1, "Scoala Gimnaziala"),
        (2, "Liceu"),

    )
    type_school = models.IntegerField(choices=STATUS_CHOICES,
                                      verbose_name="Type school", default=0)
    REQUIRED = ['name', 'addrsi ess', 'geolocation']

    def __unicode__(self):
        return self.name

    @property
    def url_link(self):
        return "/schools/" + self.slug


@receiver(pre_delete, sender=School)
def file_delete(sender, instance, **kwargs):
    # Pass false so FileField doesn't save the model.
    instance.file.delete(False)
