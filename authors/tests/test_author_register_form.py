# from django.test import TestCase
from unittest import TestCase

from django.test import TestCase as DjangoTestCase
from django.urls import reverse
from parameterized import parameterized

from authors.forms import RegisterForm

# Diferença de unittest e teste de integração.


class AuthorRegisterFormUnitTest(TestCase):
    @parameterized.expand([
        ("first_name", "Ex.: Chris"),
        ("last_name", "Ex.: Morris"),
        ("username", "Your username"),
        ("email", "Enter a valid email address"),
        ("password", "Set a password"),
        ("password2", "Repeat your password"),
    ])  # unittest
    def test_fields_placeholder(self, field, placeholder):
        form = RegisterForm()
        # pegando placeholder criado pelo django
        placeholder_test = form[field].field.widget.attrs["placeholder"]
        self.assertEqual(placeholder_test, placeholder)

    @parameterized.expand([
        ("username", """The username must contain letters, numbers, or @ _ .
        The length must be between 4 and 150 characters."""),
        ("email", "The email must be valid."),
        ("password", """Password must have at least one uppercase letter,
            one lowercase letter and one number. The length should
            be at least 8 character."""),
    ])  # unittest
    def test_fields_help_text(self, field, help_text):
        form = RegisterForm()
        # pegando placeholder criado pelo django
        help_text_test = form[field].field.help_text
        self.assertEqual(help_text_test, help_text)

    @parameterized.expand([
        ("username", "Username"),
        ("email", "Email"),
        ("password", "Password"),
        ("password2", "Repeat Password"),
    ])  # unittest
    def test_fields_label(self, field, label):
        form = RegisterForm()
        # pegando placeholder criado pelo django
        label_test = form[field].field.label
        self.assertEqual(label_test, label)


class AuthorRegisterFormIntegrationTest(DjangoTestCase):
    def setUp(self, *args, **kwargs) -> None:  # dados do formulário // válidos
        self.form_data = {
            "first_name": "John",
            "last_name": "Doe",
            "username": "johndoe",
            "email": "johndoe@example.com",
            "password": "StrongPassword1",
            "password2": "StrongPassword1"
        }
        return super().setUp(*args, **kwargs)

    @parameterized.expand([
        ("first_name", "Write your first name"),
        ("last_name", "Write your last name"),
        ("username", "This field must not be empty"),
        ("email", "Email must not be empty"),
        ("password", "Password must not be empty"),
        ("password2", "Please, repeat your password"),
    ])
    def test_fields_cannot_be_empty(self, field, message):
        self.form_data[field] = ""
        url = reverse("authors:create")
        # postando os dados que são iguais a 'self.form_data'
        # quando faz um post está chamando a url create
        response = self.client.post(url, data=self.form_data, follow=True)
        # self.assertIn(message, response.content.decode("utf-8"))

        # pegando somente erros
        self.assertIn(message, response.context["form"].errors.get(field))

    @parameterized.expand([
        ("username", "This field must not be empty"),
    ])
    def test_username_invalid_less_than_4_characters(self, field, message):
        self.form_data[field] = ""
        url = reverse("authors:register")
        # postando os dados que são iguais a 'self.form_data'
        # quando faz um post está chamando a url create
        response = self.client.post(url, data=self.form_data, follow=True)
        # self.assertIn(message, response.content.decode("utf-8"))
