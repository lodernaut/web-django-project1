from django import forms

from recipes.models import Recipe


class AuthorRecipeForm(forms.ModelForm):
    class Meta:
        model = Recipe  # informando quem é o model
        fields = (
            "title", "description", "preparation_time",
            "preparation_time_unit", "servings", "servings_unit",
            "preparation_step", "cover")
