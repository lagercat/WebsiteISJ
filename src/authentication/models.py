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
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.db import models
from django.db.models.fields.related import ForeignKey

from school.models import School
from subject.models import Subject


class ExtendedUserManager(BaseUserManager):
    def create_user(self, username, first_name, last_name, password, status=0):
        if not username:
            raise ValueError('Users must have an username')

        if not first_name:
            raise ValueError('Users must have a first name')

        if not last_name:
            raise ValueError('Users must have a last name')

        if not password:
            raise ValueError('Users must have a password')

        user = self.model(
            first_name=first_name,
            last_name=last_name,
            username=username,
            status=status
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, first_name, last_name, password):
        user = self.create_user(username, first_name, last_name, password, 3)
        user.is_admin = True
        user.status = 3
        user.save(using=self._db)
        return user


class ExtendedUser(AbstractBaseUser):
    class Meta:
        index_text = "Manage"
        verbose_name = 'User'
        verbose_name_plural = 'Users'

    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    username = models.CharField(max_length=50, unique=True)

    school = ForeignKey(School, blank=True, null=True)

    STATUS_CHOICES = (
        (0, "Personal"),
        (1, "Director"),
        (2, "Inspector"),
        (3, "Admin"),
    )
    status = models.IntegerField(choices=STATUS_CHOICES,
                                 verbose_name="user status", default=0)
    subjects = models.ManyToManyField(Subject, blank=True, null=True)

    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=(status == 3))

    objects = ExtendedUserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['first_name', 'last_name']
    
    perms = {
      0: [
        "post.view_post",
        "post.change_own_post",
        "post.add_own_post"
      ],
      1: [
        "school.change_own_school",
        "post.view_post",
        "post.change_own_post",
        "post.add_own_post"
      ],
      2: [
        "post.view_post",
        "post.change_own_post",
        "post.add_own_post",
        "event.change_own_event",
        "event.add_own_event",
        "news.change_own_news",
        "news.add_own_news",
        "subject.change_own_subjectpost",
        "subject.add_own_subjectpost",
        "subject.change_own_subcategory",
        "subject.add_own_subcategory",
        "gallery.change_own_gallery",
        "gallery.add_own_gallery",
      ],
      3: [
        "all"
      ],
    }

    def get_full_name(self):
        return self.first_name + " " + self.last_name

    def get_short_name(self):
        return self.first_name

    def __unicode__(self):
        return self.first_name + " " + self.last_name

    def has_perm(self, perm, obj=None):
        if perm == "frontend.view_module":
            return True
        if perm == "frontend.change_module":
            return False
        if "all" in self.perms[self.status] or perm in self.perms[self.status]:
            return True
        return False

    def has_module_perms(self, app_label):
        return True

    @property
    def is_staff(self):
        return True
