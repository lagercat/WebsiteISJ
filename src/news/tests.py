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
