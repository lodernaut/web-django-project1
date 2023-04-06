from django.test import TestCase
from django.urls import reverse


class RecipeURLsTest(TestCase):
    def test_recipe_home_url_is_correct(self):
        url = reverse("recipes:home")
        # testando se url é igual a barra
        self.assertEqual(url, "/")

    def test_recipe_category_url_is_correct(self):
        # args → passar argumentos em ordem → args(1,)
        # kwargs → passar um dicionário com argumentos nomeados → kwargs={"category_id": 1} # noqa: E501
        url = reverse("recipes:category", kwargs={"category_id": 1})
        self.assertEqual(url, "/recipes/category/1/")

    def test_recipe_detail_url_is_correct(self):
        url = reverse("recipes:recipe", args=(1,))
        self.assertEqual(url, "/recipes/1/")
