from django.test import TestCase, RequestFactory
from gallery.views import gallery


class GalleryTestCase(TestCase):

    def setUp(self):
        self.factory = RequestFactory()

    def test_good_page_number_gallery_view(self):
        request = self.factory.get('/album', {'page': 1})
        response = gallery(request)
        self.assertEqual(response.status_code, 200)

    def test_big_page_number_gallery_view(self):
        request = self.factory.get('/album', {'page': 99})
        response = gallery(request)
        self.assertEqual(response.status_code, 200)

    def test_negative_integer_page_number_view(self):
        request = self.factory.get('/album', {'page': -1})
        response = gallery(request)
        self.assertEqual(response.status_code, 200)

    def test_not_integer_page_number_gallery_view(self):
        request = self.factory.get('/album', {'page': 'test'})
        response = gallery(request)
        self.assertEqual(response.status_code, 200)
