import os
from pathlib import Path
from time import sleep

from django.core.cache import cache
from selenium import webdriver
from selenium.webdriver.chrome.service import Service

ROOT_PATH = Path(__file__).parent.parent
# cspell:ignore CHROMEDRIVER_NAME, CHROMEDRIVER_PATH, chromedriver-win64,
# cspell:ignore chromedriver.exe
CHROMEDRIVER_NAME = "chromedriver.exe"
CHROMEDRIVER_PATH = ROOT_PATH / "bin" / "chromedriver-win64" / CHROMEDRIVER_NAME  # noqa:501


def make_chrome_browser(*options):
    chrome_options = webdriver.ChromeOptions()
    if options is not None:
        for option in options:
            chrome_options.add_argument(option)
    if os.environ.get("SELENIUM_HEADLESS") == "1":
        chrome_options.add_argument("--headless")
    # opção para não encerrar navegador automaticamente
    chrome_options.add_experimental_option("detach", True)

    chrome_service = Service(executable_path=CHROMEDRIVER_PATH)  # type: ignore
    browser = webdriver.Chrome(service=chrome_service, options=chrome_options)
    return browser


# --headless
if __name__ == "__main__":
    browser = make_chrome_browser()
    browser.get("https://www.google.com/")
    sleep(5)
    browser.quit()


# RunServer Cache Clear
class ClearCacheMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        print("DjangoCacheClean 🧹")
        cache.clear()

    def __call__(self, request):
        response = self.get_response(request)
        return response
