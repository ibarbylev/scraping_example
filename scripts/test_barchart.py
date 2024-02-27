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
    from selenium import webdriver  # ATTENTION!!! webdriver ONLY for LOCAL VERSION!!!
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
        out = []
        driver.get('https://www.barchart.com/stocks/most-active/price-volume-leaders?viewName=fundamental&page=1')

        # first page
        wait = WebDriverWait(driver, 10)
        table = wait.until(EC.visibility_of_all_elements_located((By.XPATH, '//tbody')))
        for line in table:
            for i in range(1, 2):
                x = [item.text for item in line.find_elements_by_xpath(f'//td[{i}]')]
                print(x)
                print(len(x))
                out.append(x)

        next_page = driver.find_element_by_css_selector('a.next')
        next_page.click()

        # second page
        wait = WebDriverWait(driver, 10)
        table = wait.until(EC.visibility_of_all_elements_located((By.XPATH, '//tbody')))
        for line in table:
            for i in range(1, 2):
                x = [item.text for item in line.find_elements_by_xpath(f'//td[{i}]')]
                print(x)
                print(len(x))
                out.append(x)

        time.sleep(20)
    finally:
        driver.close()

        with open(get_save_path(filename), 'w') as f:
            json.dump({'data': out}, f)
        #     # f.write(username)

