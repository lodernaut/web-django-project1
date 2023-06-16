from django import forms

from utils.django_forms import add_class, add_label, add_placeholder


class LoginForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        add_placeholder(self.fields["username"], "Type your username")
        add_class(self.fields["username"], "register-form-username")
        add_label(self.fields["username"], "Username")

        add_placeholder(self.fields["password"], "Type your password")
        add_class(self.fields["password"], "register-form-password")
        add_label(self.fields["password"], "Password")

    username = forms.CharField()
    password = forms.CharField(
        widget=forms.PasswordInput()
    )
