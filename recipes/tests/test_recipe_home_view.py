from django.urls import resolve, reverse

from recipes import views

from .test_recipe_base import RecipeTestBase

# Create your tests here.


class RecipeHomeViewTest(RecipeTestBase):
    # teste: função de view → 'home' está correta?
    def test_recipe_home_view_function_is_correct(self):
        view = resolve(reverse("recipes:home"))
        self.assertIs(view.func, views.home)

    def test_recipe_home_view_return_status_code_200_ok(self):
        response = self.client.get(reverse("recipes:home"))
        self.assertEqual(response.status_code, 200)

    def test_recipe_home_view_loads_correct_template(self):
        response = self.client.get(reverse("recipes:home"))
        self.assertTemplateUsed(response, "recipes/pages/home.html")

    def test_recipe_home_template_shows_no_recipes_found_if_no_recipes(self):
        response = self.client.get(reverse("recipes:home"))
        self.assertIn(
            "<h1>No recipes found here</h1>",
            response.content.decode("utf-8"))

    def test_recipe_home_template_loads_recipes(self):
        # Need a recipe for this test
        self.make_recipe()

        response = self.client.get(reverse("recipes:home"))
        content = response.content.decode("utf-8")
        response_context_recipes = response.context["recipes"]

        # Check if one recipe exists
        self.assertIn("Recipe Title", content)
        self.assertEqual(len(response_context_recipes), 1)

    def test_recipe_home_template_not_load_recipes_not_published(self):
        """test recipe template does not
        load is_published=False recipes"""
        # Need a recipe for this test
        self.make_recipe(is_published=False)

        response = self.client.get(reverse("recipes:home"))
        response_context_recipes = response.context["recipes"]

        # Check if one recipe exists
        self.assertIn(
            "<h1>No recipes found here</h1>", response.content.decode("utf-8"))
        self.assertEqual(len(response_context_recipes), 0)
