import os
from random import choice
from string import ascii_uppercase

from django.test import TestCase

from contact.models import Contact
from contact.forms import CreateContactForm


class ContactModelTestCase(TestCase):

    def setUp(self, first_name="testing", last_name="testlast",
              email="test@isj.com", subject="Test the contact",
              message="messageme"):
        """ Create contact for tests """
        self.contact = Contact.objects.create(first_name=first_name,
                                              last_name=last_name,
                                              email=email, subject=subject,
                                              message=message)

    def test_create_contact(self):
        """ Test if user is created correctly """
        self.assertTrue(isinstance(self.contact, Contact))
        self.assertEqual(self.contact.email, self.contact.__unicode__())


class CreateContactFormTestCase(TestCase):

    def setUp(self):
        os.environ["RECAPTCHA_TESTING"] = "True"

    def tearDown(self):
        os.environ["RECAPTCHA_TESTING"] = "False"

    def test_required_fields(self):
        """Tests if all fields all required"""
        form = CreateContactForm({
            "first_name": "",
            "last_name": "",
            "email": "",
            "subject": "",
            "message": ""
        })
        check = True
        for field in form:
            if not field.errors:
                check = False
                break
        self.assertTrue(check)

    def test_clean_validators(self):
        """Tests validators implemented in clean functions"""
        form = CreateContactForm({
            "first_name": "tix12312",
            "last_name": "rajog323",
            "email": "notanemail",
            "subject": "Doar un titlu",
            "message": "randomstuff"
        })
        check = True
        for field in form:
            if not field.errors and field.label != "Subject":
                check = False
                break
        self.assertTrue(check)

    def test_correct_validation(self):
        """Tests validators implemented in clean functions"""
        form = CreateContactForm({
            "first_name": "FirstName",
            "last_name": "LastName",
            "email": "anactual@email.com",
            "subject": "Doar un titlu",
            "message": (''.join(choice(ascii_uppercase)
                                for i in range(51))),
            "g-recaptcha-response": "PASSED"
        })
        self.assertTrue(form.is_valid())
