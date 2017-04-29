from django.test import TestCase
from event.models import Event
from authentication.tests import ExtendedUser

class EventTestCase(TestCase):

    def create_user(self, first_name="test", last_name="forthewin",
                    username="kek", password="cevaparola", status=2):
        return ExtendedUser.objects.create_user(first_name=first_name,
                                                last_name=last_name,
                                                username=username,
                                                password=password,
                                                status=status)

    def create_event(self, name="de test", text="ca sa fie"
                     , address="Something",
                     geolocation="4,20"):
        return Event.objects.create(name=name, text=text,
                                    address=address, geolocation=geolocation,
                                    author = self.create_user())

    def test_create_event(self):
        obj = self.create_event()

        self.assertTrue(isinstance(obj, Event))
        self.assertEqual(obj.__unicode__(), obj.name)
