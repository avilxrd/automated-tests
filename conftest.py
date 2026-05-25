import pytest

from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from webdriver_manager.firefox import GeckoDriverManager
from selenium.webdriver.firefox.options import Options


@pytest.fixture(scope="session")
def driver():

    options = Options()
#    options.add_argument("--headless")

    driver = webdriver.Firefox(
        service=Service(GeckoDriverManager().install()),
        options=options
    )

    yield driver

    driver.quit()