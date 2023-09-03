from django import forms

from recipes.models import Recipe
from utils.django_forms import add_class


class AuthorRecipeForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        add_class(
            self.fields["title"], "edit-form-title")

        add_class(
            self.fields["preparation_step"],
            "edit-form-preparation-step span-2")

        add_class(self.fields["cover"], "edit-form-cover span-2")

    class Meta:
        model = Recipe  # informando quem é o model
        fields = (
            "title", "description", "preparation_time",
            "preparation_time_unit", "servings", "servings_unit",
            "preparation_step", "cover")
