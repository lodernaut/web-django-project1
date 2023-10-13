from unittest import mock
from unittest.mock import patch

from django.urls import resolve, reverse

from recipes import views

from .test_recipe_base import RecipeTestBase


# Create your tests here.
class RecipeHomeViewTest(RecipeTestBase):
    # teste: função de view → 'home' está correta?
    def test_recipe_home_view_class_is_correct(self):
        view = resolve(reverse("recipes:home"))
        self.assertIs(view.func.view_class, views.RecipeListViewHome)

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
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "recipes/pages/home.html")
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

    # mock

    def test_recipe_home_is_paginator_mock(self):
        self.make_recipe_in_batch(amount=27)

        response = self.client.get(reverse("recipes:home"))
        recipes = response.context["recipes"]

        paginator = recipes.paginator

        # criou 27 receitas → retornar 3 page
        self.assertEqual(paginator.num_pages, 3)

        # Verificando quantas receitas tem na page 1, esperado 9
        self.assertEqual(len(paginator.get_page(1)), 9)

    def test_recipe_home_is_paginator_context_manage(self):
        self.make_recipe_in_batch(amount=20)
        response = self.client.get(reverse("recipes:home"))
        self.assertEqual(response.status_code, 200)
        self.assertTrue('page_obj' in response.context)
        self.assertEqual(len(response.context['page_obj']), 9)

    def test_invalid_page_query(self):
        self.make_recipe_in_batch(amount=20)
        response = self.client.get(
            reverse("recipes:home"), {"page": "invalid"})
        self.assertEqual(response.status_code, 200)
        self.assertTrue("page_obj" in response.context)
        self.assertEqual(len(response.context["page_obj"]), 9)
