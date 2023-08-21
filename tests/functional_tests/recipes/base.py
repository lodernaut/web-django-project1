import time

# from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.test import LiveServerTestCase

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
