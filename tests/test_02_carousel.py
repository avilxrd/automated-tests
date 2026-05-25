from time import sleep

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

URL= "https://www.rwth-aachen.de"

# [3] carrousel
def test_carrousel(driver):
    driver.get(URL)

    wait = WebDriverWait(driver, 10)

    carrousel = wait.until(
        EC.visibility_of_element_located(
            (By.CLASS_NAME, 'button-list')
        )
    )
    assert carrousel
    assert carrousel.is_displayed()

    expected_option = ["Academics", "Research", "Transfer", "About RWTH"]
    expected_button = ["Explore Academics", "Explore Research", "Explore Technology Transfer", "Explore RWTH"]

    background = None

    for option in carrousel.find_elements(By.TAG_NAME, 'button'):
        assert option.is_displayed()
        assert option.get_attribute("textContent") in expected_option

        option.click()

        button_tab = driver.find_element(
            By.CSS_SELECTOR,
            "div.container.active a.button.tabbable"
        )
        assert button_tab.get_attribute('textContent') in expected_button
        assert button_tab.get_attribute("href") not in [None, ""]

        sleep(0.5)
        background_active = driver.find_element(
            By.CSS_SELECTOR,
            "div.background.active"
        ).get_attribute('id')

        assert background_active != background
        background = background_active
