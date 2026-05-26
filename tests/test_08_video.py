from time import sleep

from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

URL= "https://www.rwth-aachen.de"

def test_video(driver):
    driver.get(URL)

    wait = WebDriverWait(driver, 10)

    # abrir página de notícias
    news = wait.until(
        EC.element_to_be_clickable(
            (By.XPATH, '//*[@id="header"]/div[3]/a[1]')
        )
    )
    news.click()

    # wrapper do vídeo
    video_wrapper = wait.until(
        EC.visibility_of_element_located(
            (By.CSS_SELECTOR, '.video-wrapper')
        )
    )

    assert video_wrapper.is_displayed()

    # iframe
    iframe = wait.until(
        EC.presence_of_element_located(
            (By.CSS_SELECTOR, '.video-wrapper iframe')
        )
    )

    assert iframe is not None

    data_src = iframe.get_attribute("data-src")

    assert data_src is not None
    assert "youtube.com/embed/" in data_src
    assert "autoplay=1" in data_src

    # poster do vídeo
    poster = video_wrapper.find_element(
        By.CLASS_NAME,
        'poster-wrapper'
    )

    assert poster.is_displayed()
    assert poster.get_attribute("role") == "img"
    assert poster.get_attribute("data-type") == "youtube"

    # imagem de fundo
    style = poster.get_attribute("style")

    assert "background-image" in style

    # acessibilidade
    assert poster.get_attribute("aria-label") != ""

    # botão play
    play_button = poster.find_element(
        By.CLASS_NAME,
        'play-button'
    )

    assert play_button.is_displayed()
    assert play_button.text == "Play Video"
    assert play_button.get_attribute("role") == "button"

    # clicar no vídeo
    play_button.click()

    # popup de proteção
    popup = wait.until(
        EC.visibility_of_element_located(
            (By.CLASS_NAME, 'data-protection-wrapper')
        )
    )

    assert popup.is_displayed()

    # texto do popup
    popup_text = popup.find_element(
        By.CLASS_NAME,
        'data-protection'
    )

    assert "YouTube" in popup_text.text

    # botões
    buttons = popup.find_element(
        By.CLASS_NAME,
        'button-wrapper'
    )

    accept_button = buttons.find_element(
        By.CLASS_NAME,
        'accept'
    )

    decline_button = buttons.find_element(
        By.CLASS_NAME,
        'decline'
    )

    assert accept_button.is_displayed()
    assert decline_button.is_displayed()

    assert accept_button.text == "Accept"
    assert decline_button.text == "Decline"

    # aceitar
    accept_button.click()

    # espera iframe carregar vídeo
    wait.until(
        lambda d: "youtube.com/embed/" in d.find_element(
            By.CSS_SELECTOR,
            ".video-wrapper iframe"
        ).get_attribute("src")
    )

    iframe = driver.find_element(
        By.CSS_SELECTOR,
        ".video-wrapper iframe"
    )

    sleep(1)

    assert "youtube.com/embed/" in iframe.get_attribute("src")