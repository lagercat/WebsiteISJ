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
from django.test import TestCase

from authentication.tests import ExtendedUser
from news.models import News


class NewsTestCase(TestCase):

    @staticmethod
    def create_user(first_name="test", last_name="forthewin",
                    username="kek", password="cevaparola", status=2):
        """ Create user for tests """
        return ExtendedUser.objects.create_user(first_name=first_name,
                                                last_name=last_name,
                                                username=username,
                                                password=password,
                                                status=status)

    def create_news(self, name="de test", text="ca sa fie"):
        """ Test test news """
        return News.objects.create(name=name, text=text,
                                   author=self.create_user())

    def test_create_news(self):
        """ Test if news is created correctly"""
        obj = self.create_news()

        self.assertTrue(isinstance(obj, News))
        self.assertEqual(obj.__unicode__(), obj.name)
