from django.test import TestCase
from django.urls import reverse


class HomePageTest(TestCase):
    def test_status_code(self):
        url = reverse('home')
        self.response = self.client.get(url)
        self.assertEqual(self.response.status_code, 200)