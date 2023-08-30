import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

from tests.authors.base import AuthorsBaseTest


# Test Form
@pytest.mark.functional_test
class AuthorsRegisterTest(AuthorsBaseTest):
    def fill_form_dummy_data(self, form):
        # Encontrando todos elementos que tenham a tag 'input'
        fields = form.find_elements(By.TAG_NAME, "input")
        for field in fields:
            # enviando ' ' para todos campos que não estão invisíveis 'hidden'
            if field.is_displayed():
                field.send_keys(" "*20)

    def get_form(self):
        return self.browser.find_element(
            By.XPATH, "/html/body/main/div[2]/form")

    def form_field_test_witch_callback(self, callback):
        self.browser.get(self.live_server_url + "/authors/register/")
        form = self.get_form()

        self.fill_form_dummy_data(form)
        # para o campo de email
        form.find_element(By.NAME, "email").send_keys(Keys.CONTROL + "a")
        form.find_element(By.NAME, "email").send_keys("test@testing.com")

        # Executando callback passando o form
        callback(form)
        return form

    def test_empty_first_name_error_message(self):
        def callback(form):
            first_name_field = self.get_by_id(form, 'id_first_name')
            # first_name_field.send_keys(" ")
            first_name_field.send_keys(Keys.ENTER)

            # Selecionando novamente a pág depois do enter
            form = self.get_form()

            self.assertIn("Write your first name", form.text)
        self.form_field_test_witch_callback(callback)

    def test_empty_last_name_error_message(self):
        def callback(form):
            last_name_field = self.get_by_id(form, 'id_last_name')
            # last_name_field.send_keys(" ")
            last_name_field.send_keys(Keys.ENTER)

            # Selecionando novamente a pág depois do enter
            form = self.get_form()

            self.assertIn("Write your last name", form.text)
        self.form_field_test_witch_callback(callback)

    def test_empty_username_error_message(self):
        def callback(form):
            username_field = self.get_by_id(form, 'id_username')
            # username_field.send_keys(" ")
            username_field.send_keys(Keys.ENTER)

            # Selecionando novamente a pág depois do enter
            form = self.get_form()

            self.assertIn("This field must not be empty", form.text)
        self.form_field_test_witch_callback(callback)

    def test_invalid_email_error_message(self):
        def callback(form):
            email_field = self.get_by_id(form, 'id_email')
            # email_field.send_keys(" ")
            email_field.send_keys(Keys.ENTER)

            # Selecionando novamente a pág depois do enter
            form = self.get_form()

            self.assertIn("The email must be valid.", form.text)
        self.form_field_test_witch_callback(callback)

    def test_password_email_error_message(self):
        def callback(form):
            password1 = self.get_by_id(form, 'id_password')
            password2 = self.get_by_id(form, 'id_password2')
            # password_field.send_keys(" ")
            password1.send_keys("@Password321")
            password2.send_keys("@password321diff")
            password2.send_keys(Keys.ENTER)

            # Selecionando novamente a pág depois do enter
            form = self.get_form()

            self.assertIn("""The passwords do not match.""", form.text)
        self.form_field_test_witch_callback(callback)

    def test_user_valid_data_register_successfully(self):
        # Abrindo a pág → /authors/register/
        self.browser.get(self.live_server_url + "/authors/register/")
        form = self.get_form()

        # Selecionando o input pelo id e enviando 'First name'
        self.get_by_id(form, "id_first_name").send_keys("First name")
        self.get_by_id(form, "id_last_name").send_keys("Last name")
        self.get_by_id(form, "id_username").send_keys("username_test")
        self.get_by_id(form, "id_email").send_keys("test@testing.com")
        self.get_by_id(form, "id_password").send_keys(
            "P@ssword1234")  # spell:disable-line
        self.get_by_id(form, "id_password2").send_keys(
            "P@ssword1234")  # spell:disable-line

        form.submit()

        self.assertIn(
            "Your user is created, please log in.",
            self.browser.find_element(By.TAG_NAME, "body").text)
