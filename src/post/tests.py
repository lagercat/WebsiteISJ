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
import os

from django.test import TestCase

from authentication.models import ExtendedUser
from post.models import Post


class PostTestCase(TestCase):
        def create_user(self, first_name="test", last_name="forthewin",
                        username="kek", password="cevaparola", status=2):
            return ExtendedUser.objects.create_user(first_name=first_name,
                                                    last_name=last_name,
                                                    username=username,
                                                    password=password,
                                                    status=status)

        def create_post(self, name="de test", text="ca sa fie",
                        address="Something",
                        geolocation="4,20"):
            return Post.objects.create(author=self.create_user(),
                                       name="TestFile", file='tests/test.png')

        def test_create_post(self):
            obj = self.create_post()

            self.assertTrue(isinstance(obj, Post))
            self.assertEqual(os.path.basename(obj.file.url), obj.filename)
