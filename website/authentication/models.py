from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User


class Account(models.Model):
    __access_level__dict = {
        1: "Inspector",
        2: "Director"
    }

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    access_level = models.IntegerField(default=-1)
    # should make a school model
    # should make a subject model

    def get_access_level(self):
        return self.__statut_dict.get(self.access_level, default="Unknown")

    def validate_access_level(self):x
        return self.get_access_level() != "Unknown"
