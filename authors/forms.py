from django import forms
from django.contrib.auth.models import User


class RegisterForm(forms.ModelForm):
    class Meta:  # class Meta utilizado para passar metadados do formulário para o django
        model = User  # sendo atrelado ao model User
        fields = [  # campos que o django vai atrelar ao formulário
            "first_name",
            "last_name",
            "username",
            "email",
            "password",
        ]
