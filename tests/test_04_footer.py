from asyncio.windows_events import NULL
from time import sleep

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

URL= "https://www.rwth-aachen.de"

# [6] footer
def test_footer(driver):
    driver.get(URL)

    wait = WebDriverWait(driver, 10)

    footer = wait.until(
        EC.visibility_of_element_located(
            (By.ID, "footer")
        )
    )
    assert footer.is_displayed()

    expected_titles = [
        "Services",
        "Other Portals",
        "Further Institutions"
    ]

    titles = footer.find_elements(By.TAG_NAME, "h3")

    title_texts = [
        title.text.strip()
        for title in titles
        if title.text.strip()
    ]

    for expected in expected_titles:
        assert expected in title_texts

    links = footer.find_elements(By.TAG_NAME, "a")
    assert len(links) > 0

    for link in links:

        assert link.is_displayed()

        href = link.get_attribute("href")
        text = link.text.strip()

        assert href is not None
        assert href != ""

        if link.find_elements(By.TAG_NAME, "img") == []:
            assert text != ""

    external_links = footer.find_elements(
        By.CSS_SELECTOR,
        "a.external"
    )

    for link in external_links:
        assert link.get_attribute("target") == "_blank"

    expected_socials = [
        "Instagram",
        "LinkedIn",
        "YouTube",
        "TikTok",
        "Facebook",
        "Threads",
        "BlueSky",
        "Mastodon"
    ]

    social_section = footer.find_element(
        By.CLASS_NAME,
        "social-media"
    )

    social_links = social_section.find_elements(
        By.TAG_NAME,
        "a"
    )

    social_texts = [
        link.text.strip()
        for link in social_links
    ]

    for social in expected_socials:
        assert social in social_texts

    images = footer.find_elements(By.TAG_NAME, "img")

    assert len(images) > 0

    for img in images:

        assert img.is_displayed()

        alt = img.get_attribute("alt")

        assert alt is not None
        assert alt != ""
        assert img.get_attribute("naturalWidth") != "0"

    copyright_div = footer.find_element(
        By.CLASS_NAME,
        "copyright"
    )

    assert "RWTH Aachen University" in copyright_div.text
