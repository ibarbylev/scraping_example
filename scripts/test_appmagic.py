#!/usr/bin/env python
from datetime import datetime, date
import json
# https://selenium-python.readthedocs.io/
import time

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

from common import get_driver
from saving import get_save_path

HOSTING_LAST_DAY = datetime.strptime('2021-01-07', "%Y-%m-%d")
today = datetime.now()
days_left = (HOSTING_LAST_DAY - today).days
days_left_info = f'Until the end of the hosting lease left {days_left} days. Script was ran at {datetime.now()}'
if days_left < 0:
    days_left_info = f'Hosting lease ended {abs(days_left)} days ago!'

out = [[days_left_info, '', '']]

def run(filename, **kwargs):
    driver = get_driver()
    driver.set_page_load_timeout(600)

    print('Hello!')
    out1 = []
    try:
        driver.get('https://appmagic.rocks/top-charts/publishers?topDepth=1000&country=WW&store=2&headquarter=NT')

        # first page
        wait = WebDriverWait(driver, 15)
        # elements = wait.until(EC.visibility_of_all_elements_located((By.CLASS_NAME, 'text-overflow top-description')))
        elements = wait.until(EC.visibility_of_all_elements_located((By.CLASS_NAME, 'top-content')))
        count = -1
        for element in elements:
            count += 1
            # if count == 100:
            #     break
            if (count + 2) % 3 == 0:
                # print(count, element)
                item = element.text.split('\n')[:2]
                out1.append(item)

        print('part #2', "=" * 100)
        # second page
        out2 = []
        driver.get('https://appmagic.rocks/top-charts/publishers?topDepth=1000&country=WW&store=2&headquarter=EM')

        wait = WebDriverWait(driver, 15)
        elements = wait.until(EC.visibility_of_all_elements_located((By.CLASS_NAME, 'top-content')))
        count = -1
        for element in elements:
            count += 1
            # if count == 100:
            #     break
            if (count + 2) % 3 == 0:
                # print(count, element)
                item = element.text.split('\n')[:2]
                out2.append(item)
            # print("out2=", out2)

        out.append(out1)
        out.append(out2)

    finally:
        driver.close()

        with open(get_save_path(filename), 'w') as f:
            json.dump({'data': out}, f)
        #     # f.write(username)
