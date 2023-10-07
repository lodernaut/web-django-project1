from unittest.mock import patch

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

    @patch("recipes.views.recipe_list_view.PER_PAGE_HOME", new=3)
    def test_recipe_home_is_paginator_mock(self):
        self.make_recipe_in_batch(amount=8)

        response = self.client.get(reverse("recipes:home"))
        recipes = response.context["recipes"]

        paginator = recipes.paginator

        # criou 9 receitas → retornar 3 pág
        self.assertEqual(paginator.num_pages, 3)
        # Verificando quantas receitas tem na pág 1, esperado 3
        self.assertEqual(len(paginator.get_page(1)), 3)

    def test_recipe_home_is_paginator_context_manage(self):
        for i in range(9):  # for para 9 receitas criadas
            kwargs = {
                "author_data": {"username": f"username_test{i+1}"},
                "slug": f"slug-test-{i+1}"}
            self.make_recipe(**kwargs)

        # context manage
        with patch("recipes.views.recipe_list_view.PER_PAGE_HOME", new=3):
            response = self.client.get(reverse("recipes:home"))
            recipes = response.context["recipes"]

            paginator = recipes.paginator

            # criou 9 receitas → retornar 3 pág
            self.assertEqual(paginator.num_pages, 3)

            # Verificando quantas receitas tem na pág 1, esperado 3
            self.assertEqual(len(paginator.get_page(1)), 3)

    def test_invalid_page_query_uses_page_one(self):
        self.make_recipe_in_batch(amount=8)

        with patch('recipes.views.recipe_list_view.PER_PAGE_HOME', new=3):
            response = self.client.get(reverse('recipes:home') + '?page=12A')
            self.assertEqual(
                response.context['recipes'].number,
                1
            )
            response = self.client.get(reverse('recipes:home') + '?page=2')
            self.assertEqual(
                response.context['recipes'].number,
                2
            )
            response = self.client.get(reverse('recipes:home') + '?page=3')
            self.assertEqual(
                response.context['recipes'].number,
                3
            )
