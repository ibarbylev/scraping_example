#!/usr/bin/env python

import json
# https://selenium-python.readthedocs.io/
import time

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
    print('Hello!')

    try:
        driver.get('http://www.yarmarka-ryazan.ru/personal/my-ads/')

        email_input = driver.find_element_by_name('USER_LOGIN')
        email_input.send_keys("it4each.com@gmail.com")

        password_input = driver.find_element_by_name('USER_PASSWORD')
        password_input.send_keys("Aasdf1")

        button = driver.find_element_by_name('Login')
        button.click()

        driver.get('http://www.yarmarka-ryazan.ru/personal/my-ads/?login=yes')

        username = driver.find_element_by_class_name('top-cabinet__link').text
        time.sleep(3)
    finally:
        driver.close()

        with open(get_save_path(filename), 'w') as f:
            json.dump({'username': username}, f)
            # f.write(username)

