from django import forms
from django.contrib.auth.models import User


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
        add_placeholder(self.fields["username"], "Your username")
        add_class(self.fields["username"], "register-form-username")
        add_label(self.fields["username"], "Usuário")

        add_placeholder(self.fields["email"], "Enter a valid email address")
        add_class(self.fields["email"], "register-form-email")

        add_placeholder(self.fields["first_name"], "Ex.: Chris")
        add_class(self.fields["first_name"], "register-form-name")

        add_placeholder(self.fields["last_name"], "Ex.: Morris")
        add_class(self.fields["last_name"], "register-form-name")

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
        error_messages={"required": "Password must not be empty"},
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
