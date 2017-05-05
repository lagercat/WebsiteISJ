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
