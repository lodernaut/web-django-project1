from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse


class AuthorLogoutTest(TestCase):
    def test_user_tries_to_logout_using_get_method(self):
        User.objects.create_user(
            username="username_test", password="P@ssword123")
        # django já possui um client com login (não é necessário usar live_server_url como no selenium 'teste funcional') # noqa:E501
        self.client.login(username="username_test", password="P@ssword123")
        response = self.client.get(reverse("authors:logout"))

        self.assertEqual(response.status_code, 302)

    def test_user_tries_to_logout_another_user(self):
        User.objects.create_user(
            username="username_test", password="P@ssword123")
        self.client.login(username="username_test", password="P@ssword123")
        response = self.client.post(reverse("authors:logout"), data={
            "username": "another_username",
            "password": "P@ssword123",
        }, follow=True)

        self.assertIn("Invalid logout user", response.content.decode("utf-8"))
