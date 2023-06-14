from django.test import TestCase

from authors.forms import RegisterForm


class TestRegisterForm(TestCase):
    def test_placeholder(self):
        form = RegisterForm()
        self.assertEqual(
            form.fields["first_name"].widget.attrs["placeholder"], "Ex.: Chris")
        self.assertEqual(
            form.fields["last_name"].widget.attrs["placeholder"], "Ex.: Morris")
        self.assertEqual(
            form.fields["username"].widget.attrs["placeholder"], "Your username")
        self.assertEqual(
            form.fields["email"].widget.attrs["placeholder"], "Enter a valid email address")
        self.assertEqual(
            form.fields["password"].widget.attrs["placeholder"], "Set a password")
        self.assertEqual(
            form.fields["password2"].widget.attrs["placeholder"], "Repeat your password")