from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

URL= "https://www.rwth-aachen.de"

# [7] language-changer
def test_language_changer(driver):
    driver.get(URL)

    wait = WebDriverWait(driver, 10)

    lang_changer = wait.until(
        EC.visibility_of_element_located(
            (By.CLASS_NAME, "language-changer")
        )
    )
    assert lang_changer.is_displayed()

    title_before = driver.title
    before = lang_changer.get_attribute("title")

    lang_changer.click()

    lang_changer = wait.until(
        EC.visibility_of_element_located(
            (By.CLASS_NAME, "language-changer")
        )
    )
    assert title_before != driver.title
    assert before != lang_changer.get_attribute("title")