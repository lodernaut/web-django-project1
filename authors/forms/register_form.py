from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

from utils.django_forms import (add_class, add_label, add_placeholder,
                                strong_password)


class RegisterForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        add_placeholder(self.fields["first_name"], "Ex.: Chris")
        add_class(self.fields["first_name"], "register-form-name")

        add_placeholder(self.fields["last_name"], "Ex.: Morris")
        add_class(self.fields["last_name"], "register-form-name")

        add_placeholder(self.fields["username"], "Your username")
        add_class(self.fields["username"], "register-form-username")
        add_label(self.fields["username"], "Username")

        add_placeholder(self.fields["email"], "Enter a valid email address")
        add_class(self.fields["email"], "register-form-email")
        add_label(self.fields["email"], "Email")

        add_placeholder(self.fields["password"], "Set a password")
        add_class(self.fields["password"], "register-form-password")
        add_label(self.fields["password"], "Password")

        add_placeholder(self.fields["password2"], "Repeat your password")
        add_class(self.fields["password2"], "register-form-password")
        add_label(self.fields["password2"], "Repeat Password")
    # sobrescrevendo
    first_name = forms.CharField(
        error_messages={"required": "Write your first name"}
    )
    last_name = forms.CharField(
        error_messages={"required": "Write your last name"}
    )
    username = forms.CharField(
        error_messages={
            "required": "This field must not be empty",
            "min_length": "Make sure the username is at least 4 characters long",  # noqa: E501
            "max_length": "Make sure the username has a maximum of 150 characters",  # noqa: E501
        },
        help_text=("""The username must contain letters, numbers, or @ _ .
        The length must be between 4 and 150 characters."""),
        min_length=4, max_length=150,
    )
    email = forms.EmailField(
        required=True,
        widget=forms.TextInput(),
        error_messages={"required": "Email must not be empty"},
        help_text=("The email must be valid."),
    )
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

    def clean_email(self):
        email = self.cleaned_data.get("email", "")
        # check se já existe na base de dados // capturando usuário que tem email=email
        exists = User.objects.filter(email=email).exists()

        if exists:
            raise ValidationError(
                "User email is already in use", code="invalid")

        return email

    def clean(self):  # precisa pegar o valor que vem do campo → 'data' vem os dados cru do formulário sem nenhuma limpeza // cleaned_data vem os dados tratados pelo django, é um dicionário com as chave sendo o nome dos campo → self.cleaned_data.get("password")
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
