# Unittest
import time

# from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.test import LiveServerTestCase
from selenium.webdriver.common.by import By

from utils.browser import make_chrome_browser


class RecipeBaseFunctionalTest(LiveServerTestCase):
    def setUp(self) -> None:
        # responsável por criar o browser
        self.browser = make_chrome_browser()
        return super().setUp()

    def tearDown(self) -> None:
        self.sleep(2)
        self.browser.quit()
        return super().tearDown()

    def sleep(self, seconds=5):
        time.sleep(seconds)


class RecipeHomePageFunctionalTest(RecipeBaseFunctionalTest):
    def test_recipe_home_page_without_recipes_not_found_messages(self):
        # fazendo uma get so servidor // self.live_server_url abre o servido automaticamente sem precisar link # noqa:501
        self.browser.get(self.live_server_url)
        body = self.browser.find_element(By.TAG_NAME, "body")
        self.assertIn("No recipes found here", body.text)
