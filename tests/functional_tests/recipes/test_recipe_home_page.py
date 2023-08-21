
import pytest
from selenium.webdriver.common.by import By

from tests.functional_tests.recipes.base import RecipeBaseFunctionalTest


@pytest.mark.functional_test
class RecipeHomePageFunctionalTest(RecipeBaseFunctionalTest):
    def test_recipe_home_page_without_recipes_not_found_messages(self):
        # fazendo uma get so servidor // self.live_server_url abre o servido automaticamente sem precisar link # noqa:501
        self.browser.get(self.live_server_url)
        body = self.browser.find_element(By.TAG_NAME, "body")
        self.assertIn("No recipes found here", body.text)
