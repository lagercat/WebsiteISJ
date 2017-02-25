from __future__ import unicode_literals

from django.db import models
from utility.models import CustomPermissionsMixin
from django_google_maps import fields as map_fields


class School(CustomPermissionsMixin):
    class Meta(CustomPermissionsMixin.Meta):
        abstract = False
        verbose_name = "School"
        verbose_name_plural = "Schools"
        index_text = "Manage"

    name = models.CharField(max_length=100, null=True)
    telephone = models.CharField(max_length=11, null=True)
    fax = models.CharField(max_length=15, blank=True)
    email = models.EmailField(max_length=20, blank=True)
    website = models.CharField(max_length=100, blank=True)
    address = map_fields.AddressField(max_length=200)
    geolocation = map_fields.GeoLocationField(max_length=100)

    def __unicode__(self):
        return self.name
