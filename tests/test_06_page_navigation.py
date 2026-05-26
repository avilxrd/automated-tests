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

def test_it_center_slider(driver):
    driver.get(URL)

    wait = WebDriverWait(driver, 10)

    quick_access_btn = wait.until(
        EC.element_to_be_clickable(
            (By.ID, 'quick-start-control')
        )
    )
    quick_access_btn.click()

    it_center = wait.until(
        EC.element_to_be_clickable(
            (By.XPATH, '//*[@id="quick-start"]/div/div[2]/div[3]/ul/li[2]/a')
        )
    )
    it_center.click()

    driver.switch_to.window(driver.window_handles[-1])

    # botoes de controle
    control_wrapper = wait.until(
        EC.presence_of_element_located(
            (By.CLASS_NAME, 'control-wrapper')
        )
    )

    prev = control_wrapper.find_element(
        By.XPATH,
        '//*[@id="main"]/div[1]/div[2]/div[1]'
    )

    next = control_wrapper.find_element(
        By.XPATH,
        '//*[@id="main"]/div[1]/div[2]/div[3]'
    )

    slider_grid = wait.until(
        EC.presence_of_element_located(
            (By.CLASS_NAME, 'item-rack')
        )
    )

    divs = slider_grid.find_elements(
        By.CLASS_NAME,
        'item-wrapper'
    )

    def assert_slider_changes(button):
        old_style = slider_grid.get_attribute('style')

        button.click()

        wait.until(
            lambda d: slider_grid.get_attribute('style') != old_style
        )

        new_style = slider_grid.get_attribute('style')

        assert old_style != new_style

    for _ in divs:
        assert_slider_changes(next)

    for _ in divs:
        assert_slider_changes(prev)