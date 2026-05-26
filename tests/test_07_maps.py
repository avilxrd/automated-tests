from time import sleep

from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

URL= "https://www.rwth-aachen.de"

def test_maps(driver):
    driver.get(URL)
    wait = WebDriverWait(driver, 30)

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

    address = wait.until(
        EC.visibility_of_element_located(
            (By.CLASS_NAME, 'adr')
        )
    )

    link = address.find_element(
        By.TAG_NAME, 'a'
    )
    link.click()

    driver.switch_to.window(driver.window_handles[-1])

    # caixa de diálogo
    dialog_box = wait.until(
        EC.presence_of_element_located(
            (By.CLASS_NAME, 'ui-dialog-buttonset')
        )
    )

    options = dialog_box.find_elements(
        By.TAG_NAME, 'button'
    )

    accept = None
    for option in options:
        if option.text == "Accept":
            accept = option
            accept.click()
            break

    #
    headline = wait.until(
        EC.visibility_of_element_located(
            (By.CLASS_NAME, 'headline-bg')
        )
    )

    headline_name = wait.until(
        EC.visibility_of_element_located(
            (By.CSS_SELECTOR, '.headline-bg .name')
        )
    )
    assert headline_name.text == "IT Center [ITC] [022000]"

    headline_addr = wait.until(
        EC.visibility_of_element_located(
            (By.CSS_SELECTOR, '.headline-bg .address')
        )
    )
    assert headline_addr.text == "Administrative Organization - Seffenter Weg 23, 52074 Aachen"

    infos = wait.until(
        EC.visibility_of_all_elements_located(
            (By.CSS_SELECTOR, '.additionalInfos .additionalElement')
        )
    )

    assert len(infos) == 4

    expected_names = [
        "Nachrichtentechnische Zentrale [5360]",
        "Kackertstr. 10 [3038]",
        "IT Center Erweiterungsbau [2191]",
        "IT Center (ehem. Rechenzentrum) [2190]"
    ]

    expected_addrs = [
        "Seffenter Weg 23, 52074 Aachen",
        "Kopernikusstr. 6, 52074 Aachen",
        "Kackertstr. 10, 52072 Aachen",
        "Wendlingweg 10, 52074 Aachen"
    ]

    for info in infos:
        name = info.find_element(By.CLASS_NAME, 'name')
        assert name.text in expected_names
        addr = info.find_element(By.CLASS_NAME, 'address')
        assert addr.text in expected_addrs

    # rota
    infos[0].click()

    calc_route = wait.until(
        EC.visibility_of_element_located(
            (By.XPATH, '//*[@id="overlayInfo"]/div[1]/div[1]/div[1]')
        )
    )

    calc_route.click()

    starting_point = wait.until(
        EC.visibility_of_element_located(
            (By.XPATH, '//*[@id="startNav"]')
        )
    )
    starting_point.send_keys("rwth"+Keys.RETURN)

    wait.until(
        lambda d: starting_point.get_attribute("value")
                  != 'rwth'
    )

    assert starting_point.get_attribute("value") == (
        'Klinikum der RWTH Aachen, "Uniklinik" [5980]'
    )

    # calcular rotas
    calculate_route = wait.until(
        EC.visibility_of_element_located(
            (By.XPATH, '//*[@id="calcRouteButton"]')
        )
    )

    calculate_route.click()

    routes_options = wait.until(
        EC.visibility_of_element_located(
            (By.CLASS_NAME, 'adp-fullwidth')
        )
    )

    routes = routes_options.find_elements(By.TAG_NAME, 'tr')

    routes_list = []
    for r in routes:
        if r.get_attribute("jstcache") == "151":
            routes_list.append(r)

    assert len(routes_list) == 3

    for r in routes_list:
        r.click()

        sleep(0.5)

        directions_list = wait.until(
            EC.visibility_of_element_located(
                (By.CLASS_NAME, 'adp-directions')
            )
        )

        directions = directions_list.find_elements(By.TAG_NAME, 'tr')
        assert len(directions) > 0
