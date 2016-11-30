from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User


class Account(models.Model):
    __access_level__dict = {
        1 : "Inspector",
        2 : "Director"
    }

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    access_level = models.IntegerField(default=-1)

    def get_access_level(self):
        return self.__statut_dict.get(self.statut, default="Unknown")

    def validate_acces_level(self):
        return self.get_acces_lever != "Unknown"
