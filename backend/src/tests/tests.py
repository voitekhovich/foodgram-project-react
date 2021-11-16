from http import HTTPStatus
from django.test import Client, TestCase


class StaticPagesURLTests(TestCase):
    def setUp(self):
        self.guest_client = Client()

    def test_about_url_exists_at_desired_location(self):
        """Проверка доступности страниц."""
        response = self.guest_client.get('/')
        self.assertEqual(response.status_code, HTTPStatus.OK)

        response = self.guest_client.get('/admin/')
        self.assertEqual(response.status_code, HTTPStatus.OK)

        response = self.guest_client.get('/api/docs/')
        self.assertEqual(response.status_code, HTTPStatus.OK)
