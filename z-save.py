from django import forms
from django.contrib.auth.models import User


def add_attr(field, attr_name, attr_new_val):
    existing_attr = field.widget.attrs.get(attr_name, "")
    field.widget.attr[attr_name] = f"{existing_attr} {attr_new_val}".strip()


class RegisterForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        add_attr(self.fields["username"], "placeholder", "Your username")

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
                "placeholder": "Enter a valid email address"}),
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
