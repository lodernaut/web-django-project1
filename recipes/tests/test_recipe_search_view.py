from django.urls import resolve, reverse

from recipes import views

from .test_recipe_base import RecipeTestBase

# Create your tests here.


class RecipeSearchViewTest(RecipeTestBase):
    def test_recipe_search_uses_correct_view_function(self):
        resolved = resolve(reverse("recipes:search"))
        self.assertIs(resolved.func, views.search)

    def test_recipe_search_loads_correct_view_function(self):
        response = self.client.get(reverse("recipes:search") + "?q=test")
        self.assertTemplateUsed(response, "recipes/pages/search.html")

    def test_recipe_search_raises_404_if_no_search_term(self):
        response = self.client.get(reverse("recipes:search"))
        self.assertEqual(response.status_code, 404)

    def test_search_return_404_in_white_space(self):
        response = self.client.get(reverse("recipes:search") + "?q=+")
        self.assertEqual(response.status_code, 404)

    def test_recipe_search_term_is_on_page_title_and_escaped(self):
        url = reverse('recipes:search') + "?q=<Test>"  # <> ← tag HTML
        response = self.client.get(url)
        self.assertIn(
            "Search for &#x27;&lt;Test&gt;&#x27;",
            response.content.decode("utf-8")
        )
