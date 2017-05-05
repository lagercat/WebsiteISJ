import random
import string

from django.test import TestCase

from .models import *


class ExtendedUserManagerTestCase(TestCase):
    def setUp(self):
        pass

    def test_create_user(self):
        """Tests if user is created successfully."""
        user = ExtendedUser.objects.create_user("roadd", "garo", "adi", "dadadada98", 2)
        self.assertEqual(user.username, "roadd")
        self.assertEqual(user.first_name, "garo")
        self.assertEqual(user.last_name, "adi")
        self.assertTrue(user.check_password("dadadada98"))
        self.assertEqual(user.status, 2)

    def test_create_superuser(self):
        """Tests if superuser is created successfully."""
        user = ExtendedUser.objects.create_superuser("mrroadd", "garo", "adi", "dadadada98")
        self.assertEqual(user.username, "mrroadd")
        self.assertEqual(user.first_name, "garo")
        self.assertEqual(user.last_name, "adi")
        self.assertTrue(user.check_password("dadadada98"))
        self.assertEqual(user.status, 3)


class ExtendedUserTestCase(TestCase):
    def setUp(self):
        self.personal = ExtendedUser.objects.create_user("roadd0", "garo", "adi", "dadadada98", 0)
        self.director = ExtendedUser.objects.create_user("roadd1", "garo", "adi", "dadadada98", 1)
        self.inspector = ExtendedUser.objects.create_user("roadd2", "garo", "adi", "dadadada98", 2)
        self.admin = ExtendedUser.objects.create_user("roadd3", "garo", "adi", "dadadada98", 3)

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
            self.admin.has_perm(r''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(20))))
