from django.core.exceptions import ValidationError
from parameterized import parameterized

from .test_recipe_base import Recipe, RecipeTestBase


class RecipeModelTest(RecipeTestBase):
    def setUp(self) -> None:
        self.recipe = self.make_recipe()
        return super().setUp()

    def make_recipe_no_defaults(self):
        recipe = Recipe(
            category=self.make_category("Test Default Category"),
            author=self.make_author(username="TestDefaultCategory"),
            title='Recipe Title',
            description='Recipe Description',
            slug='recipe-slug-no-defaults',
            preparation_time=10,
            preparation_time_unit='Minutos',
            servings=5,
            servings_unit='Porções',
            preparation_step='Recipe Preparation Steps')
        recipe.full_clean()  # Fazendo ocorre as validações
        recipe.save()  # salvando na base de dados
        return recipe

    @parameterized.expand([
        ("title", 65),
        ("description", 165),
        ("preparation_time_unit", 65),
        ("servings_unit", 65),
    ])
    def test_recipe_max_length(self, field, max_length):
        setattr(self.recipe, field, "X" * (max_length + 1))
        with self.assertRaises(ValidationError):
            self.recipe.full_clean()

    def test_recipe_preparation_step_is_html_is_false_by_default(self):
        recipe = self.make_recipe_no_defaults()

        # check if it's false
        self.assertFalse(
            recipe.preparation_step_is_html,
            msg="preparation_step_is_html → is not False")

    def test_recipe_is_published_is_false_by_default(self):
        recipe = self.make_recipe_no_defaults()

        self.assertFalse(
            recipe.is_published,
            msg="is_published → is not False")

    # testando se retorna string
    def test_recipe_string_representation(self):
        needed = 'Testing Representation'
        self.recipe.title = needed
        self.recipe.full_clean()
        self.recipe.save()
        self.assertEqual(
            str(self.recipe), needed,
            msg=f'Recipe string representation must be '
                f'"{needed}" but "{str(self.recipe)}" was received.'
        )
