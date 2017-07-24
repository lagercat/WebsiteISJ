import random
import string
import os
from random import choice
from string import ascii_uppercase

from django.test import TestCase
from django.contrib.auth.models import User

from authentication.models import ExtendedUser
from authentication.forms import LoginForm, ResetPasswordForm


class ExtendedUserManagerTestCase(TestCase):

    def setUp(self):
        pass

    def test_create_user(self):
        """Tests if user is created successfully."""
        user = ExtendedUser.objects.create_user(
            "roadd", "garo", "adi", "dadadada98", 2)
        self.assertEqual(user.username, "roadd")
        self.assertEqual(user.first_name, "garo")
        self.assertEqual(user.last_name, "adi")
        self.assertTrue(user.check_password("dadadada98"))
        self.assertEqual(user.status, 2)

    def test_create_superuser(self):
        """Tests if superuser is created successfully."""
        user = ExtendedUser.objects.create_superuser(
            "mrroadd", "garo", "adi", "dadadada98")
        self.assertEqual(user.username, "mrroadd")
        self.assertEqual(user.first_name, "garo")
        self.assertEqual(user.last_name, "adi")
        self.assertTrue(user.check_password("dadadada98"))
        self.assertEqual(user.status, 3)


class ExtendedUserTestCase(TestCase):

    def setUp(self):
        self.personal = ExtendedUser.objects.create_user(
            "roadd0", "garo", "adi", "dadadada98", 0)
        self.director = ExtendedUser.objects.create_user(
            "roadd1", "garo", "adi", "dadadada98", 1)
        self.inspector = ExtendedUser.objects.create_user(
            "roadd2", "garo", "adi", "dadadada98", 2)
        self.admin = ExtendedUser.objects.create_user(
            "roadd3", "garo", "adi", "dadadada98", 3)

    def test_permissions_personal(self):
        """Tests personal account permissions."""
        self.assertTrue(self.personal.has_perm("frontend.view_module"))
        self.assertFalse(self.personal.has_perm("frontend.change_module"))
        for i in self.personal.perms[self.personal.status]:
            self.assertTrue(self.personal.has_perm(i))

    def test_permissions_director(self):
        """Tests personal account permissions."""
        self.assertTrue(self.director.has_perm("frontend.view_module"))
        self.assertFalse(self.director.has_perm("frontend.change_module"))
        for i in self.director.perms[self.director.status]:
            self.assertTrue(self.director.has_perm(i))

    def test_permissions_inspector(self):
        """Tests personal account permissions."""
        self.assertTrue(self.inspector.has_perm("frontend.view_module"))
        self.assertFalse(self.inspector.has_perm("frontend.change_module"))
        for i in self.inspector.perms[self.inspector.status]:
            self.assertTrue(self.inspector.has_perm(i))

    def test_permissions_admin(self):
        """Tests personal account permissions."""
        self.assertTrue(self.admin.has_perm("frontend.view_module"))
        self.assertFalse(self.admin.has_perm("frontend.change_module"))
        self.assertTrue(
            self.admin.has_perm(r''.join(random.choice(string.ascii_uppercase +
                                                       string.digits) for _ in range(20))))


class LoginFormTestCase(TestCase):

    def setUp(self):
        os.environ["RECAPTCHA_TESTING"] = "True"

    def tearDown(self):
        os.environ["RECAPTCHA_TESTING"] = "False"

    def test_required_username(self):
        """Tests required condition for username field"""
        form = LoginForm({
            "username": "",
            "password": "password",
            "recaptcha_response_field": "PASSED"
        })
        self.assertFalse(form.is_valid())

    def test_required_password(self):
        """Tests required condition for password field"""
        form = LoginForm({
            "username": "username",
            "password": "",
            "recaptcha_response_field": "PASSED"
        })
        self.assertFalse(form.is_valid())

    def test_required_recaptcha(self):
        """Tests required condition for recaptcha field"""
        form = LoginForm({
            "username": "username",
            "password": "password",
            "recaptcha_response_field": ""
        })
        self.assertFalse(form.is_valid())

    def test_username_maxlen(self):
        """Tests max length attribute of username field"""
        form_instace = LoginForm()
        field_length = form_instace.fields['username'].max_length
        django_length = User._meta.get_field('username').max_length
        self.assertEqual(field_length, django_length)
        random_username = (''.join(choice(ascii_uppercase)
                                   for i in range(field_length + 1)))
        form = LoginForm({
            "username": random_username,
            "password": "password",
            "recaptcha_response_field": ""
        })
        self.assertFalse(form.is_valid())


class ResetPasswordFormTestCase(TestCase):
    def test_required_old_password(self):
        """Tests required condition for old_password field"""
        form = LoginForm({
            "old_password": "",
            "new_password": "password",
            "new_password_check": "password"
        })
        self.assertFalse(form.is_valid())

    def test_required_password(self):
        """Tests required condition for password field"""
        form = LoginForm({
            "old_password": "password",
            "new_password": "",
            "new_password_check": "password"
        })
        self.assertFalse(form.is_valid())

    def test_required_recaptcha(self):
        """Tests required condition for recaptcha field"""
        form = LoginForm({
            "old_password": "password",
            "new_password": "password",
            "new_password_check": ""
        })
        self.assertFalse(form.is_valid())
