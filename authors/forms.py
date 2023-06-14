import re

from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError


def strong_password(password):
    # utilizando expressão regular para validar password
    # positive lookahead
    regex = re.compile(r"^(?=.*[a-z])(?=.*[A-Z])(?=.*[0-9]).{8,}$")

    if not regex.match(password):
        raise ValidationError(
            ("""Password must have at least one uppercase letter,
            one lowercase letter and one number. The length should
            be at least 8 character."""), code="invalid")


def add_attr(field, attr_name, attr_new_val):
    existing_attr = field.widget.attrs.get(attr_name, "")
    field.widget.attrs[attr_name] = f"{existing_attr} {attr_new_val}".strip()


def add_placeholder(field, placeholder_val):
    field.widget.attrs["placeholder"] = placeholder_val


def add_class(field, class_val):
    field.widget.attrs["class"] = class_val


def add_label(field, label_val):
    field.label = label_val


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
            "min_length": "Make sure the username is at least 4 characters long",
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
