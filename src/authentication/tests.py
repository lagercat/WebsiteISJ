import random
import string
import os
from random import choice
from string import ascii_uppercase

from django.test import TestCase, Client
from django.contrib.auth.models import User

from authentication.models import ExtendedUser
from authentication.forms import (LoginForm, ResetPasswordForm,
                                  ExtendedUserCreationFormAdmin)
from school.models import School
from subject.models import Subject


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
            self.admin.has_perm(r''.join(
                random.choice(string.ascii_uppercase +
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


class ExtendedUserCreationFormAdminTestCase(TestCase):

    def setUp(self):
        self.school = School.objects.create(
            name="TestSchool",
            geolocation="23,24",
            address="test"
        )
        self.subject = Subject.objects.create(
            name="TestSubject"
        )
        self.input = {
            "username": "test_username",
            "first_name": "Tuxi",
            "last_name": "Pinguinescu",
            "school": School.objects.filter(slug=self.school.slug),
            "is_active": True,
            "password1": "pass1",
            "password2": "pass1",
            "subjects": Subject.objects.filter(id=self.subject.id),
            "status": 0
        }

    def test_empty_password(self):
        """Tests required condition for password fields"""
        inp = self.input
        inp["password1"] = ""
        inp["password2"] = ""
        form = ExtendedUserCreationFormAdmin(self.input)
        self.assertFalse(form.is_valid())

    def test_same_check_password(self):
        """Tests equality condition for password fields"""
        inp = self.input
        inp["password2"] = "test"
        form = ExtendedUserCreationFormAdmin(self.input)
        self.assertFalse(form.is_valid())

    def test_available_status_choices(self):
        """Tests if the form's status choices are the same with the user's"""
        form_instace = ExtendedUserCreationFormAdmin()
        form_choices = form_instace.fields['status'].choices
        user_status_choices = ExtendedUser.STATUS_CHOICES
        restult = True
        for first, second in zip(form_choices, user_status_choices):
            for a, b in zip(first, second):
                to_comp_f = a
                to_comp_s = b
                if isinstance(to_comp_f, dict):
                    to_comp_f = to_comp_f['label']
                if isinstance(to_comp_s, dict):
                    to_comp_s = to_comp_s['label']
                if to_comp_f != to_comp_s:
                    restult = False
                    break
            if not restult:
                break
        self.assertTrue(restult)

    def test_correct_director(self):
        """Tests positbility to create a headmaster"""
        form_instace = ExtendedUserCreationFormAdmin()
        form_choices = form_instace.fields['status'].choices
        director_status = [x[0] for x in form_choices if x[1] == "Director"][0]
        inp = self.input
        inp["status"] = int(director_status)
        inp["subjects"] = None
        form = ExtendedUserCreationFormAdmin(inp)
        self.assertTrue(form.is_valid())

    def test_empty_school(self):
        """Tests positbility to create a headmaster without a school"""
        form_instace = ExtendedUserCreationFormAdmin()
        form_choices = form_instace.fields['status'].choices
        director_status = [x[0] for x in form_choices if x[1] == "Director"][0]
        inp = self.input
        inp["status"] = int(director_status)
        inp["school"] = None
        inp["subjects"] = None
        form = ExtendedUserCreationFormAdmin(inp)
        self.assertFalse(form.is_valid())

    def test_wrong_school_permission(self):
        """Tests positbility to create any other permission
         but a headmaster with a school"""
        form_instace = ExtendedUserCreationFormAdmin()
        form_choices = form_instace.fields['status'].choices
        inp = self.input
        inp["subjects"] = None
        response = True
        for x in form_choices:
            if x[1] != "Director":
                inp["status"] = x[0]
                form = ExtendedUserCreationFormAdmin(inp)
                if form.is_valid():
                    response = False
        self.assertTrue(response)

    def test_correct_inspector(self):
        """Tests positbility to create a inspector"""
        form_instace = ExtendedUserCreationFormAdmin()
        form_choices = form_instace.fields['status'].choices
        director_status = [x[0]
                           for x in form_choices if x[1] == "Inspector"][0]
        inp = self.input
        inp["status"] = int(director_status)
        inp["school"] = None
        form = ExtendedUserCreationFormAdmin(inp)
        self.assertTrue(form.is_valid())

    def test_empty_subject(self):
        """Tests positbility to create an inspector without a subject"""
        form_instace = ExtendedUserCreationFormAdmin()
        form_choices = form_instace.fields['status'].choices
        inspector_status = [x[0]
                            for x in form_choices if x[1] == "Inspector"][0]
        inp = self.input
        inp["status"] = inspector_status
        inp["subjects"] = None
        inp["school"] = None
        form = ExtendedUserCreationFormAdmin(inp)
        self.assertFalse(form.is_valid())

    def test_wrong_subject_permission(self):
        """Tests positbility to create a any other permission
         but an inspector with a subject"""
        form_instace = ExtendedUserCreationFormAdmin()
        form_choices = form_instace.fields['status'].choices
        inp = self.input
        inp["school"] = None
        response = True
        for x in form_choices:
            if x[1] != "Inspector":
                inp["status"] = x[0]
                form = ExtendedUserCreationFormAdmin(inp)
                if form.is_valid():
                    response = False
                    break
        self.assertTrue(response)


class AuthenticationViewsTestCase(TestCase):

    def setUp(self):
        self.client = Client()
        self.user_unecrypt_pass = "pass123"
        self.user = ExtendedUser.objects.create_user(
            "test_user", "Tuxi", "Pinguinescu", self.user_unecrypt_pass, 0)
        os.environ["RECAPTCHA_TESTING"] = "True"

    def tearDown(self):
        os.environ["RECAPTCHA_TESTING"] = "False"

    def test_login_view(self):
        """Tests if login view works with right credetials and right
         recaptcha"""
        login_response = self.client.post('/login/', data={
            "username": self.user.username,
            "password": self.user_unecrypt_pass,
            "g-recaptcha-response": "PASSED"
            })
        self.assertEqual(login_response.wsgi_request.user, self.user)

    def test_wrong_login_view(self):
        """Tests if login view works with wrong credetials and right
         recaptcha"""
        login_response = self.client.post('/login/', data={
            "username": self.user.username + "rand",
            "password": self.user_unecrypt_pass,
            "g-recaptcha-response": "PASSED"
            })
        self.assertNotEqual(login_response.wsgi_request.user, self.user)

    def test_login_view_captcha(self):
        """Tests if login view works with right
        credetials and wrong recaptcha"""
        login_response = self.client.post('/login/', data={
            "username": self.user.username,
            "password": self.user_unecrypt_pass,
            "g-recaptcha-response": "PASED"
            })
        self.assertNotEqual(login_response.wsgi_request.user, self.user)

    def test_wrong_login_view_captcha(self):
        """Tests if login view works with wrong
        credetials and wrong recaptcha"""
        login_response = self.client.post('/login/', data={
            "username": self.user.username + "rand",
            "password": self.user_unecrypt_pass,
            "g-recaptcha-response": "PASED"
            })
        self.assertNotEqual(login_response.wsgi_request.user, self.user)
