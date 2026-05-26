from asyncio.windows_events import NULL
from time import sleep

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

URL= "https://www.rwth-aachen.de"

# [4] images read-more
def test_teaser_wrapper(driver):
    driver.get(URL)

    teaser_wrapper = driver.find_element(
        By.CLASS_NAME,
        "teaser-wrapper"
    )

    imgs = teaser_wrapper.find_elements(By.TAG_NAME, "img")

    # scroll
    driver.execute_script(
        "arguments[0].scrollIntoView({block: 'center'});",
        imgs[0]
    )

    for img in imgs:
        sleep(0.5)
        assert img.is_displayed()
        assert img.get_attribute("src") != ""
        assert img.get_attribute("alt") != NULL

    links = teaser_wrapper.find_elements(By.LINK_TEXT, "Read More")

    for link in links:
        assert link.get_attribute("href") is not None
        #print(link.get_attribute("href"))

# [5] div expansion
def test_div_expansion(driver):
    driver.get(URL)

    wait = WebDriverWait(driver, 10)

    inner_wrapper = wait.until(
        EC.presence_of_element_located((By.CLASS_NAME, "inner-wrapper"))
    )

    item_rack = wait.until(
        EC.presence_of_element_located((By.CSS_SELECTOR, ".inner-wrapper .item-rack"))
    )

    frames        = inner_wrapper.find_elements(By.CLASS_NAME, "grid-wrapper")

    style = None

    for frame in frames:
        frame.click()
        assert item_rack.get_attribute("style") != style
        style = item_rack.get_attribute("style")
