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
        driver.get('https://www.slickcharts.com/sp500')
        wait = WebDriverWait(driver, 10)

        # lines = driver.find_element_by_xpath('//tbody')
        # print(lines.text)
        table = wait.until(EC.visibility_of_all_elements_located((By.XPATH, '//tbody')))
        out = []
        for line in table:
            for i in range(1, 8):
                x = [item.text for item in line.find_elements_by_xpath(f'//td[{i}]')]
                print(x)
                out.append(x)

        # for table in wait.until(
        #         EC.visibility_of_all_elements_located((By.XPATH, '//tbody'))):
        #     # for items in table.find_elements_by_xpath('//tr'):
        #     data = [item.text for item in table.find_elements_by_xpath('//td')]
        #     print(data)

            # data = [item.text for items in table.find_elements_by_xpath('//tr') for item in items.find_elements_by_xpath('//td')]
            # print(data)

        # class ="setTriggeredClass(row)" data-ng-attr-title="[[ setLinkTitle(row, key) ]]" data-ng-href="/stocks/quotes/AAPL/overview" data-ng-bind="cell" title="" href="/stocks/quotes/AAPL/overview" > AAPL < / a >
        # email_input.send_keys("it4each.com@gmail.com")
        #
        # password_input = driver.find_element_by_name('USER_PASSWORD')
        # password_input.send_keys("Aasdf1")
        #
        # button = driver.find_element_by_name('Login')
        # button.click()
        #
        # driver.get('http://www.yarmarka-ryazan.ru/personal/my-ads/?login=yes')
        #
        # username = driver.find_element_by_class_name('top-cabinet__link').text
        time.sleep(3)
    finally:
        driver.close()

        with open(get_save_path(filename), 'w') as f:
            json.dump({'username': out}, f)
        #     # f.write(username)

