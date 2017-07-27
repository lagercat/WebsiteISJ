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
