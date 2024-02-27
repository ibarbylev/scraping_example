#!/usr/bin/env python
# https://it4each.com/media/scraping/mV8fy0XCwUgzfuu6ji2IO9kzqobgcbZXu+wEUISLOH4=.json
import gc
import json
import logging
# https://selenium-python.readthedocs.io/
from datetime import datetime
import time
import traceback

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.common.exceptions import WebDriverException
from common import get_driver, log_memory_usage
from saving import get_save_path

from bs4 import BeautifulSoup
import csv
import requests

logger = logging.getLogger(__name__)


SCROLL_STEP = 100
SCROLL_PAUSE = 0.5

HOSTING_LAST_DAY = datetime.strptime('2020-12-05', "%Y-%m-%d")
today = datetime.now()
days_left = (HOSTING_LAST_DAY - today).days
days_left_info = f'Script was ran at {datetime.now()}'
if days_left < 0:
    days_left_info = f'Hosting lease ended {abs(days_left)} days ago!'

urls = ['https://kazanexpress.ru/vsemvsem']


def parse_url(url):
    # print("Loading next URL")
    # # disable images start =================
    # chrome_options = webdriver.ChromeOptions()
    # prefs = {"profile.managed_default_content_settings.images": 2}
    # chrome_options.add_experimental_option("prefs", prefs)
    # driver = webdriver.Chrome(chrome_options=chrome_options)
    # # disable images end ====================

    driver = get_driver()
    try:

        driver.get(url)
        wait = WebDriverWait(driver, 10)

        wait.until(EC.visibility_of_all_elements_located((By.CLASS_NAME, 'card-info-block')))

        # Scroll to the bottom of the page
        # driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        # wait.until(EC.invisibility_of_element((By.CSS_SELECTOR, '[loader-spinner-spinner]')))

        all_names = []
        for i in range(100_000):
            time.sleep(SCROLL_PAUSE)
            # Scroll by 100px
            # Error: stale element reference: element is not attached to the page document
            # means we're scrolling too fast.
            driver.execute_script(f"window.scrollBy(0, {SCROLL_STEP});")

            finished = driver.execute_script("return window.scrollY + window.innerHeight >= document.body.scrollHeight;")
            if finished:
                break

            names = driver.find_elements_by_css_selector('.card-info-block')
            names = [n.text.strip() for n in names]
            all_names.extend(names)
            print(len(names))

        all_names = set(all_names)
        print("All collected:", len(all_names))
        # quantity = t.text.split()[0]
        # t = wait.until(EC.visibility_of_element_located((By.CLASS_NAME, 'new-price')))
        # price = t.text.split()[0]

        # return [url, quantity, price]
        return [url, names, names]
    finally:
        try:
            driver.close()
            driver.quit()
        except WebDriverException:
            logger.exception("Closing failed")

        gc.collect()


def run(filename, **kwargs):
    # selenium.common.exceptions.InvalidArgumentException:
    # driver.get("https:::google.com")

    # selenium.common.exceptions.WebDriverException: Message: unknown error: net::ERR_NAME_NOT_RESOLVED
    # driver.get("https://googleeee.com")

    # 404 - no exception
    # driver.get("https://google.com/eeee")

    out = [[days_left_info, '', '']]
    url = urls[0]
    retries = 0
    while retries < 3:
        retries += 1
        try:
            log_memory_usage()

            url, quantity, price = parse_url(url)
            print([url, quantity, price])
            out.append([url, quantity, price])

            log_memory_usage()
            break
        except WebDriverException:
            logger.exception("Error while loading URL")

    if days_left < 0:
        out = out[0]
    out[0][2] = f' and was ended at {datetime.now().time()}'
    with open(get_save_path(filename), 'w') as f:
        json.dump({'data': out}, f)
