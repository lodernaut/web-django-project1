import re

from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError


def strong_password(password):
    regex = re.compile(r"^(?=.*[a-z])(?=.*[A-Z])(?=.*[0-9]).{8,}$")

    if not regex.match(password):
        raise ValidationError(
            ("""Password must have at least one uppercase letter,
            one lowercase letter and one number. The length should
            be at least 8 character."""), code="invalid")


class RegisterForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
    password = forms.CharField(
        required=True,
        widget=forms.PasswordInput(),
        error_messages={"required": "Password must not be empty"},
        help_text=(
            """Password must have at least one uppercase letter,
            one lowercase letter and one number. The length should
            be at least 8 character."""),
        validators=[strong_password]
    )
    password2 = forms.CharField(
        required=True,
        widget=forms.PasswordInput(),
        error_messages={"required": "Please, repeat your password"},
    )

    class Meta:
        model = User
        fields = [
            "first_name",
            "last_name",
            "username",
            "email",
            "password",
        ]

    # precisa pegar o valor que vem do campo → 'data' vem os dados cru do formulário sem nenhuma limpeza // cleaned_data vem os dados tratados pelo django, é um dicionário com as chave sendo o nome dos campo → self.cleaned_data.get("password")

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        password2 = cleaned_data.get("password2")

        if password != password2:
            # atrelando o erro a chave password
            password_confirmation_error = ValidationError(  # envolvendo o erro em ValidationError
                "The passwords do not match.",
                code="invalid")
            raise ValidationError({
                # atrelando o erro a chave password usando variável
                "password": password_confirmation_error,

                "password2": [  # atrelando erro a uma lista
                    "The passwords do not match.", "Another error"
                ]})
