from django.test import TestCase
from django.urls import reverse


# Create your tests here.
class MainAppTest(TestCase):
    def test_index_view(self):
        response = self.client.get(reverse("main:index"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "main/index.html")
        self.assertContains(response, "Chat App")
