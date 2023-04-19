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

    def test_recipe_search_can_find_recipe_by_title_1(self):
        response = self.client.get(
            reverse('recipes:search') + "?q=<RecipeSearchTest>")
        self.make_recipe(title="RecipeSearchTest")

        self.assertIn(
            "RecipeSearchTest", response.content.decode("utf-8"))

    def test_recipe_search_can_find_recipe_by_title_2(self):
        title1 = "This is recipe one"
        title2 = "This is recipe two"

        recipe1 = self.make_recipe(
            slug="one", title=title1, author_data={"username": "one"}
        )
        recipe2 = self.make_recipe(
            slug="two", title=title2, author_data={"username": "two"}
        )

        search_url = reverse("recipes:search")
        response1 = self.client.get(f"{search_url}?q={title1}")
        response2 = self.client.get(f"{search_url}?q={title2}")
        response_both = self.client.get(f"{search_url}?q=this")

        self.assertIn(recipe1, response1.context["recipes"])
        self.assertNotIn(recipe2, response1.context["recipes"])

        self.assertIn(recipe2, response2.context["recipes"])
        self.assertNotIn(recipe1, response2.context["recipes"])

        self.assertIn(recipe1, response_both.context["recipes"])
        self.assertIn(recipe2, response_both.context["recipes"])
