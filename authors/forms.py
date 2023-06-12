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
        add_label(self.fields["username"], "Usuário")

        add_placeholder(self.fields["email"], "Enter a valid email address")
        add_class(self.fields["email"], "register-form-email")

    password = forms.CharField(
        required=True,
        widget=forms.PasswordInput(
            attrs={
                "class": "register-form-password",
                "placeholder": "Set a password"}),
        label="Password",
        error_messages={"required": "Password must not be empty"},
        help_text=(
            """Password must have at least one uppercase letter,
            one lowercase letter and one number. The length should
            be at least 8 character."""),
        validators=[strong_password]
    )
    password2 = forms.CharField(
        required=True,
        widget=forms.PasswordInput(
            attrs={
                "class": "register-form-password",
                "placeholder": "Repeat your password"}),
        label="Repeat Password",
        error_messages={"required": "Password must not be empty"},
    )
    email = forms.CharField(
        required=True,
        widget=forms.TextInput(
            attrs={
                "class": "register-form-email",
            }),
        label="Email",
        error_messages={"required": "Email must not be empty"},
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

    def clean_password(self):
        data = self.cleaned_data.get("password")
        # exemplo removendo a palavra 'atenção' de dentro do campo password
        if "atenção" in data:
            raise ValidationError(
                "Não digite '%(value)s' no campo password.",
                code="invalid",
                params={"value": "atenção"}  # para recuperar o value)
            )
        return data

    def clean_first_name(self):
        data = self.cleaned_data.get('first_name')

        if "John Doe" in data:
            raise ValidationError(
                "Não digite '%(value)s' no campo first name",
                code="invalid",
                params={"value": "John Doe"}
            )

        return data

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
