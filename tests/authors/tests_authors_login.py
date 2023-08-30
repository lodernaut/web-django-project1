import pytest
from django.contrib.auth.models import User
from django.test import Client, TestCase
from django.urls import reverse
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

from tests.authors.base import AuthorsBaseTest


@pytest.mark.functional_test
class AuthorsLoginTest(AuthorsBaseTest):
    def test_user_valid_data_can_login_success(self):
        str_password = "P@ssword123"
        # Necessita apenas de usuário e senha
        user = User.objects.create_user(
            username="user_test", password=str_password)  # noqa:E501, cspell:disable-line

        # user open login page
        self.browser.get(
            self.live_server_url + reverse("authors:login"))  # forma dinâmica

        # user viewing login form
        form = self.browser.find_element(By.CLASS_NAME, "main-form")
        username_field = self.get_by_id(form, "id_username")
        password_field = self.get_by_id(form, "id_password")

        # user enter data
        username_field.send_keys(user.username)
        password_field.send_keys(str_password)

        # user submit form
        # password_field.send_keys(Keys.ENTER) ou
        form.submit()

        # end test
        self.assertIn(
            "Your are logged in.",
            self.browser.find_element(By.TAG_NAME, "body").text)

    def test_login_create_raises_404_if_not_post_method(self):
        # se usuário fizer um get
        self.browser.get(
            self.live_server_url + reverse("authors:login_create"))

        self.assertIn("Not Found", self.browser.find_element(
            By.TAG_NAME, "body").text)

    def test_login_invalid_credential(self):
        str_password = "P@ssword123"
        user = User.objects.create_user(
            username="username_test", password=str_password)

        self.browser.get(self.live_server_url + reverse("authors:login"))

        form = self.browser.find_element(By.CLASS_NAME, "main-form")

        username_field = self.get_by_id(form, "id_username")
        password_field = self.get_by_id(form, "id_password")

        username_field.send_keys(user.username)
        password_field.send_keys(str_password + "1")

        form.submit()

        self.assertIn("Invalid credentials.", self.browser.find_element(
            By.TAG_NAME, "body").text)
        self.sleep(5)

    def test_login_invalid_username_or_password(self):
        self.browser.get(self.live_server_url + reverse("authors:login"))

        form = self.browser.find_element(By.CLASS_NAME, "main-form")

        username_field = self.get_by_id(form, "id_username")
        password_field = self.get_by_id(form, "id_password")

        username_field.send_keys("test_username")
        password_field.send_keys(" ")

        form.submit()

        self.assertIn(
            "Invalid username or password.",
            self.browser.find_element(By.TAG_NAME, "body").text)

    def test_login_valid(self):
        str_password = "P@ssword123"
        user = User.objects.create_user(
            username="username_test", password=str_password)

        self.browser.get(self.live_server_url + reverse("authors:login"))

        form = self.browser.find_element(By.CLASS_NAME, "main-form")
        username_field = self.get_by_id(form, "id_username")
        password_field = self.get_by_id(form, "id_password")

        username_field.send_keys(user.username)
        password_field.send_keys(str_password)
        form.submit()

        self.assertIn(
            "Your are logged in.",
            self.browser.find_element(By.TAG_NAME, "body").text)
