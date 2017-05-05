from django.test import TestCase
from contact.models import Contact


class ContactTestCase(TestCase):

    @staticmethod
    def create_contact(first_name="testing", last_name="testlast",
                       email="test@isj.com", subject="Test the contact",
                       message="messageme"):
        """ Create contact for tests """
        return Contact.objects.create(first_name=first_name, last_name=last_name,
                                      email=email, subject=subject,
                                      message=message)

    def test_create_contact(self):
        """ Test if user is created correctly """
        obj = self.create_contact()

        self.assertTrue(isinstance(obj, Contact))
        self.assertEqual(obj.email, obj.__unicode__())
