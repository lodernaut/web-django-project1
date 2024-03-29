from unittest.mock import patch

import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

from tests.functional_tests.recipes.base import RecipeBaseFunctionalTest


@pytest.mark.functional_test
class RecipeHomePageFunctionalTest(RecipeBaseFunctionalTest):
    @patch("recipes.views.all.PER_PAGE_HOME", new=3)
    def test_recipe_home_page_without_recipes_not_found_messages(self):
        # fazendo uma get do servidor // self.live_server_url abre o servido automaticamente sem precisar link # noqa:501
        self.browser.get(self.live_server_url)
        body = self.browser.find_element(By.TAG_NAME, "body")
        self.assertIn("No recipes found here", body.text)

    def test_recipe_search_input_can_find_correct_recipes(self):
        recipes = self.make_recipe_in_batch(amount=3)

        title = "This is what i need"
        recipes[2].title = title
        recipes[2].save()
        self.browser.get(self.live_server_url)  # user open page
        search_input = self.browser.find_element(
            By.XPATH, "//input[@placeholder='search for a recipe ...']"
        )
        search_input.send_keys(title)
        search_input.send_keys(Keys.ENTER)
        self.assertIn(title, self.browser.title)

    def test_recipe_home_page_pagination(self):
        self.make_recipe_in_batch(amount=12)

        # Navigate to the home page
        self.browser.get(self.live_server_url)

        page2 = self.browser.find_element(
            By.XPATH, "/html/body/main/nav/div/ul/a[2]")  # ← usuário clicando na pág 2
        page2.click()

        recipe_elements = self.browser.find_elements(
            By.CLASS_NAME, "recipe")   # puxando elementos da pág
        self.assertEqual(len(recipe_elements), 3)
