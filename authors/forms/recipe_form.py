from collections import defaultdict

from django import forms

from recipes.models import Recipe
from utils.django_forms import ValidationError, add_class, add_label
from utils.strings import is_positive_number


class AuthorRecipeForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._my_errors = defaultdict(list)

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

    def clean(self, *args, **kwargs):
        super_clean = super().clean()
        cleaned_data = self.cleaned_data

        title = cleaned_data.get("title")

        description = cleaned_data.get("description")

        if title == description:
            self._my_errors["title"].append("Cannot be equal to description.")
            self._my_errors["description"].append("Cannot be equal to title.")

        # levantando/tratando erro
        if self._my_errors:
            raise ValidationError(self._my_errors)

        return super_clean

    def clean_title(self):
        title = self.cleaned_data.get("title")
        if len(title) < 5:
            self._my_errors["title"].append("Title must have at last 5 chars.")
        return title

    def clean_preparation_time(self):
        preparation_time = self.cleaned_data.get("preparation_time")
        if not is_positive_number(preparation_time):
            self._my_errors["preparation_time"].append(
                "Must be a positive number.")
        return preparation_time

    def clean_servings(self):
        servings = self.cleaned_data.get("servings")
        if not is_positive_number(servings):
            self._my_errors["servings"].append(
                "Must be a positive number.")
        return servings
