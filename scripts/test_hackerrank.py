#!/usr/bin/env python

import json
# https://selenium-python.readthedocs.io/
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

from saving import get_save_path


def run(filename, **kwargs):
    from selenium import webdriver
    from selenium.webdriver.chrome.options import Options

    options = Options()
    options.add_argument('--no-sandbox')

    driver = webdriver.Chrome(chrome_options=options,
                              # service_args=[
                              #     '--verbose',
                              #     '--log-path=/opt/django-apps/it4each/scraping/selenium.log'
                              # ]
                              )
    try:
        driver.get('https://www.hackerrank.com/auth/login')

        email_input = driver.find_element_by_css_selector('form.form [name="username"]')
        email_input.send_keys("it4each.com@gmail.com")

        password_input = driver.find_element_by_css_selector('form.form [name="password"]')
        password_input.send_keys("Aasdf1")

        button = driver.find_element_by_css_selector('form.form button.auth-button')
        button.click()

        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, ".username")),
        )

        username_elem = driver.find_element_by_css_selector('.username')
        username = username_elem.text
    finally:
        driver.close()

    with open(get_save_path(filename), 'w') as f:
        json.dump({'username': username}, f)
