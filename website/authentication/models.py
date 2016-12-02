from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User

from school.models import School
from subject.models import Subject


class Account(models.Model):
    __access_level__dict = {
        1: "Inspector",
        2: "Director"
    }

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    school = models.ForeignKey(School, related_name='accounts', blank=False, null=True, default=-1,
                               on_delete=models.PROTECT)
    access_level_code = models.IntegerField(default=-1)
    subject_one = models.ForeignKey(Subject, related_name='primers', blank=False, null=True, default=-1,
                                    on_delete=models.PROTECT)
    subject_two = models.ForeignKey(Subject, related_name='seconds', blank=False, null=True, default=-1,
                                    on_delete=models.PROTECT)
    school_three = models.ForeignKey(Subject, related_name='thirds', blank=False, null=True, default=-1,
                                     on_delete=models.PROTECT)

    @property
    def access_level(self):
        return self.__access_level__dict.get(self.access_level_code, "Unknown")

    def validate_access_level(self):
        return self.access_level != "Unknown"
