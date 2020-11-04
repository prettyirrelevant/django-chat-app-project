from django.contrib.auth import get_user_model
from django.urls import reverse
from django.test import TestCase

# Create your tests here.


class UserAppTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="testuser", email="test@test.com", password="testtesttest"
        )

    def test_user_model(self):
        user = get_user_model().objects.get(pk=1)
        self.assertEqual(str(user), "test@test.com")
        self.assertEqual(user.username, "testuser")
        self.assertEqual(user.is_admin, False)
        self.assertTrue(user.password)

    def test_get_register_view(self):
        response = self.client.get(reverse("users:register"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "users/register.html")

    def test_post_register_view(self):
        response = self.client.post(
            reverse("users:register"),
            {
                "username": "eniola",
                "email": "eniola@eniola.com",
                "password1": "eniolaeniola",
                "password2": "eniolaeniola",
            },
        )
        self.assertEqual(response.status_code, 302)

    def test_get_login_view(self):
        response = self.client.get(reverse("users:login"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "users/login.html")

    def test_post_login_view(self):
        response = self.client.post(
            reverse("users:login"),
            {"username": "test@test.com", "password": "testtesttest"},
        )
        self.assertEqual(response.status_code, 302)

    def test_profile_view(self):
        self.client.login(username="test@test.com", password="testtesttest")
        r = self.client.get(reverse("users:profile"))
        self.assertEqual(r.status_code, 200)
        self.assertTemplateUsed(r, "users/profile.html")
