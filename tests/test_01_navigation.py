from time import sleep

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

URL= "https://www.rwth-aachen.de"

def test_open_site(driver):
    driver.get(URL)
    assert "RWTH Aachen University" in driver.title

# [1] top-bar
def test_top_bar(driver):
    driver.get(URL)

    wait = WebDriverWait(driver, 10)

    # testa a visibilidade da barra de navegação
    top_bar = wait.until(
        EC.visibility_of_element_located(
            (By.CLASS_NAME, "top-bar")
        )
    )
    assert top_bar.is_displayed()

    # verifica se existe o elemento News e se ele tem um link
    news = top_bar.find_element(
        By.LINK_TEXT,
        "News"
    )
    assert news.is_displayed()
    assert news.get_attribute("href") is not None

    # verifica se existe o elemento "information for..."
    information = top_bar.find_element(
        By.ID,
        "persona-control"
    )
    assert information.is_displayed()
    assert information.text == "Information for..."
    assert information.get_attribute("role") == "button"

    # verifica se existe o elemento "quick access"
    quick_access = top_bar.find_element(
        By.ID,
        "quick-start-control"
    )
    assert quick_access.is_displayed()

    # vê se expande ao clicar
    quick_access_expanded = driver.find_element(
        By.ID,
        "quick-start"
    )

    assert quick_access_expanded.get_attribute("aria-expanded") == "false"
    quick_access.click()
    sleep(0.5)
    assert quick_access_expanded.get_attribute("aria-expanded") == "true"
    quick_access.click()
    sleep(0.5)
    assert quick_access_expanded.get_attribute("aria-expanded") == "false"

    # verifica se existe o elemento "language-changer"
    de = top_bar.find_element(
        By.CLASS_NAME,
        "language-changer"
    )
    assert de.is_displayed()
    assert de.text == "DE"

    # verifica se existe o elemento "easy-english"
    easy = top_bar.find_element(
        By.CLASS_NAME,
        "easy-english"
    )
    assert easy.is_displayed()

# [2] main navigation
def test_main_nav(driver):
    driver.get(URL)

    wait = WebDriverWait(driver, 10)

    main_nav = driver.find_element(
        By.ID, "main-nav"
    )
    assert main_nav

    main_nav_btn = wait.until(
        EC.visibility_of_element_located(
            (By.XPATH, '//*[@id="main-nav-control"]')
        )
    )
    assert main_nav_btn
    assert main_nav_btn.is_displayed()

    assert main_nav.get_attribute("aria-expanded") == "false"
    main_nav_btn.click()
    assert main_nav.get_attribute("aria-expanded") == "true"

    spans = main_nav.find_elements(
        By.CSS_SELECTOR,
        ".top-tier button span"
    )

    assert len(spans) == 5
    expected = ["Academics", "Research", "Transfer", "About RWTH", "Faculties"]

    for span in spans:
        assert span.get_attribute("textContent") in expected

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
