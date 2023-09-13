from collections import defaultdict

from django import forms

from recipes.models import Recipe
from utils.django_forms import add_class, add_label


class AuthorRecipeForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        add_class(
            self.fields["title"], "edit-form-title")

        add_class(
            self.fields["description"], "edit-form-description")

        add_class(
            self.fields["preparation_time"], "edit-form-preparation-time")

        add_class(
            self.fields["preparation_time_unit"],
            "edit-form-preparation-time-unit")

        add_class(self.fields["servings"], "edit-form-servings")

        add_class(self.fields["servings_unit"], "edit-form-servings-unit")

        add_label(self.fields["preparation_step"], "Preparation steps")
        add_class(
            self.fields["preparation_step"],
            "edit-form-preparation-step")

        add_class(self.fields["category"], "edit-form-category")

        add_label(self.fields["cover"], "Image for your recipe")
        add_class(self.fields["cover"], "edit-form-cover")

    class Meta:
        model = Recipe  # informando quem é o model
        fields = (
            "title", "description", "preparation_time",
            "preparation_time_unit", "servings", "servings_unit",
            "preparation_step", "category", "cover")
        widgets = {
            "cover": forms.FileInput(),  # file'arquivo' comum

            "servings_unit": forms.Select(  # criando campo de select
                choices=(  # choice é uma tupla de tuplas
                    ("Porções", "Porções"),  # Value:Display
                    ("Fatias", "Fatias"),
                    ("Pessoas", "Pessoas"),
                    ("Copo", "Copo"),
                )),

            "preparation_time_unit": forms.Select(  # criando campo de select
                choices=(
                    ("Minuto(s)", "Minuto(s)"),  # Value:Display
                    ("Hora(s)", "Hora(s)"),
                ))
        }
