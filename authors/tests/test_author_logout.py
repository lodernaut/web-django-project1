from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse


class AuthorLogoutTest(TestCase):
    # Testando se for enviado get ao invés de post redireciona para login
    def test_user_tries_to_logout_using_get_method(self):
        User.objects.create_user(
            username="username_test", password="P@ssword123")
        # django já possui um client com login (não é necessário usar live_server_url como no selenium 'teste funcional') # noqa:E501
        self.client.login(username="username_test", password="P@ssword123")
        response = self.client.get(reverse("authors:logout"))

        self.assertEqual(response.status_code, 302)

    # User_x não pode deslogar user_y
    def test_user_tries_to_logout_another_user(self):
        User.objects.create_user(
            username="username_test", password="P@ssword123")
        self.client.login(username="username_test", password="P@ssword123")
        response = self.client.post(reverse("authors:logout"), data={
            "username": "another_username",
            "password": "P@ssword123",
        }, follow=True)

        self.assertIn("Invalid logout user", response.content.decode("utf-8"))

    # confirmando que realizou logout
    def test_user_can_logout_successfully(self):
        User.objects.create_user(
            username="username_test", password="P@ssword123")
        self.client.login(username="username_test", password="P@ssword123")

        response = self.client.post(reverse("authors:logout"), data={  # inserido data devido a view de logou verificar  verifica se o nome de usuário enviado na requisição POST corresponde ao nome de usuário do usuário atualmente logado.
            "username": "username_test"
        }, follow=True)

        self.assertIn(
            "You have successfully logged out.",
            response.content.decode("utf-8"))
