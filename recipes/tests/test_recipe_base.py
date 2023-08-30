from django.test import TestCase

from recipes.models import Category, Recipe, User


class RecipeMixin():
    # recebendo parâmetro name e deixando padrão "Category"
    def make_category(self, name="Category"):
        return Category.objects.create(name=name)

    def make_author(
            self,
            first_name="User",
            last_name="Name",
            username="username",
            email="testing@devrecipe.com",
            password="test2023"):

        return User.objects.create_user(
            first_name=first_name,
            last_name=last_name,
            username=username,
            email=email,
            password=password)

    def make_recipe(
            self,
            category_data=None,
            author_data=None,
            title='Recipe Title',
            description='Recipe Description',
            slug='recipe-slug',
            preparation_time=10,
            preparation_time_unit='Minutos',
            servings=5,
            servings_unit='Porções',
            preparation_step='Recipe Preparation Steps',
            preparation_step_is_html=False,
            is_published=True):

        if category_data is None:
            category_data = {}
        if author_data is None:
            author_data = {}

        return Recipe.objects.create(
            category=self.make_category(**category_data),  # ← desempacotamento
            author=self.make_author(**author_data),
            title=title,
            description=description,
            slug=slug,
            preparation_time=preparation_time,
            preparation_time_unit=preparation_time_unit,
            servings=servings,
            servings_unit=servings_unit,
            preparation_step=preparation_step,
            preparation_step_is_html=preparation_step_is_html,
            is_published=is_published)

    def make_recipe_in_batch(self, amount=10):
        recipes = []
        for i in range(amount):
            kwargs = {
                "title": f"Recipe Title {i}º - Test",
                'slug': f'r{i}',
                'author_data': {'username': f'u{i}'}
            }
            recipe = self.make_recipe(**kwargs)
            recipes.append(recipe)
        return recipes


class RecipeTestBase(TestCase, RecipeMixin):
    def setUp(self) -> None:
        return super().setUp()
