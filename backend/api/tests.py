from http import HTTPStatus

from django.test import Client, TestCase


class TaskiAPITestCase(TestCase):
    def setUp(self):
        self.guest_client = Client()

    def test_api_exists(self):
        """Проверка доступности api."""
        response = self.guest_client.get('/api/')
        self.assertEqual(response.status_code, HTTPStatus.OK)
