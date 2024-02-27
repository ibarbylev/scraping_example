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

    try:
        driver.get('https://mail.ru/')

        email_input = driver.find_element_by_id("mailbox:login")
        email_input.send_keys("it4each")

        button = driver.find_element_by_css_selector('input.o-control')
        # class ="o-control" type="submit" value="Ввести пароль" >
        button.click()

        WebDriverWait(driver, 10).until(
             EC.presence_of_element_located((By.ID, 'mailbox:password')))
        # driver.get('https://mail.ru/')

        input_password = driver.find_element_by_id("mailbox:password")
        input_password.send_keys('Aasdf123')

        button = driver.find_element_by_css_selector('input.o-control')
        # class ="o-control" type="submit" value="Ввести пароль" >
        button.click()


        time.sleep(20)
    finally:
        driver.close()

        # with open(get_save_path(filename), 'w') as f:
        #     json.dump({'username': out}, f)
        # #     # f.write(username)

