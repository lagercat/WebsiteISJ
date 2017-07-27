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
