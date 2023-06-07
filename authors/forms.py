from django import forms
from django.contrib.auth.models import User


class RegisterForm(forms.ModelForm):  # formulário de ModelForm
    class Meta:  # class Meta utilizado para passar metadados do formulário para o django
        model = User  # sendo atrelado ao model User
        fields = [  # campos que o django vai atrelar ao formulário
            "first_name",
            "last_name",
            "username",
            "email",
            "password",
        ]
        labels = {
            "first_name": "First Name",
            "last_name": "Last Name",
            "username": "Username",
            "email": "Email",
            "password": "Password",
        }
        help_texts = {
            "username": "Apenas letras, números e @/./+/-/_",
        }
        error_messages = {
            "username": {
                "required": "This field must not be empty.",
                "invalid": "this field is invalid."
            },
        }
        widgets = {
            "username": forms.TextInput(attrs={
                "placeholder": "Type your username here."
            }),
            "password": forms.PasswordInput(attrs={
                "placeholder": "Type your password here."
            }),
        }
