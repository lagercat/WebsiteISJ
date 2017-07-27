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
from django.test.client import Client


class GalleryTestCase(TestCase):

    def setUp(self):
        self.client = Client()

    def test_good_page_number_gallery_view(self):
        """ Test gallery pagination with good integer """
        session = self.client.session
        session['page'] = 1
        session.save()
        response = self.client.get('/album')
        self.assertEqual(response.status_code, 200)

    def test_big_page_number_gallery_view(self):
        """ Test gallery pagination with too big integer"""
        session = self.client.session
        session['page'] = 99
        session.save()
        response = self.client.get('/album')
        self.assertEqual(response.status_code, 200)

    def test_negative_integer_page_number_view(self):
        """ Test gallery pagination with small integer """
        session = self.client.session
        session['page'] = -1
        session.save()
        response = self.client.get('/album')
        self.assertEqual(response.status_code, 200)

    def test_not_integer_page_number_gallery_view(self):
        """ Test gallery pagination with not an integer """
        session = self.client.session
        session['page'] = 'test'
        session.save()
        response = self.client.get('/album')
        self.assertEqual(response.status_code, 200)
