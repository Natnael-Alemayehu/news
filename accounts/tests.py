from django.test import TestCase
from django.contrib.auth import get_user_model


# Create your tests here.
class UsersManagersTests(TestCase):
    def test_create_user(self):
        User = get_user_model()
        user = User.objects.create_user(
            username="testUsername",
            email="testEmail@gmail.com",
            password="password",
        )
        self.assertEqual(user.username, "testUsername")
        self.assertEqual(user.email, "testEmail@gmail.com")
        self.assertTrue(user.is_active)
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)

    def test_create_superuser(self):
        User = get_user_model()
        admin_user = User.objects.create_superuser(
            username="admin",
            email="admin@gmail.com",
            password="adminpassword",
        )
        self.assertEqual(admin_user.username, "admin")
        self.assertEqual(admin_user.email, "admin@gmail.com")
        self.assertTrue(admin_user.is_active)
        self.assertTrue(admin_user.is_staff)
        self.assertTrue(admin_user.is_superuser)
