from time import sleep

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

URL= "https://www.rwth-aachen.de"

def test_text_box(driver):
    driver.get(URL)
    wait = WebDriverWait(driver, 10)

    quick_access_btn = wait.until(
        EC.element_to_be_clickable(
            (By.ID, 'quick-start-control')
        )
    )
    quick_access_btn.click()

    link_page = wait.until(
        EC.element_to_be_clickable(
            (By.XPATH, '//*[@id="quick-start"]/div/div[2]/div[3]/ul/li[6]/a')
        )
    )
    link_page.click()

    driver.switch_to.window(driver.window_handles[-1])

    search_bar = wait.until(
        EC.presence_of_element_located(
            (By.CSS_SELECTOR, "input#main-searchbar")
        )
    )

    submit_btn = wait.until(
        EC.presence_of_element_located(
            (By.XPATH, '//*[@id="search-wrapper"]/div/form/div/input[2]')
        )
    )

    assert search_bar.is_displayed()
    assert search_bar.is_enabled()
    assert search_bar.get_attribute('placeholder') == 'Enter a search term ...'

    search_bar.send_keys("computer science")
    assert search_bar.get_attribute('value') == 'computer science'
    submit_btn.click()

    results = wait.until(
        EC.presence_of_element_located(
            (By.CSS_SELECTOR, "table.results")
        )
    )
    assert results.is_displayed()
    sleep(2)

    search_bar = wait.until(
        EC.presence_of_element_located(
            (By.CSS_SELECTOR, "input#main-searchbar")
        )
    )
    search_bar.clear()
    assert search_bar.get_attribute('value') == ''
    sleep(2)