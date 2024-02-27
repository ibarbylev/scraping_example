#!/usr/bin/env python
# https://it4each.com/media/scraping/mV8fy0XCwUgzfuu6ji2IO9kzqobgcbZXu+wEUISLOH4=.json
import gc
import json
import logging
import os
# https://selenium-python.readthedocs.io/
from datetime import datetime, date
from typing import List
import time

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import WebDriverException
from common import get_driver, log_memory_usage, get_last_run_status, RunStatus, update_pid_file, delete_pid_file
from saving import get_save_path

from bs4 import BeautifulSoup
import requests

logger = logging.getLogger(__name__)

HOSTING_LAST_DAY = datetime.strptime('2020-12-05', "%Y-%m-%d")
today = datetime.now()
days_left = (HOSTING_LAST_DAY - today).days
days_left_info = f'Until the end of the hosting lease left {days_left} days. Script was ran at {datetime.now()}'
if days_left < 0:
    days_left_info = f'Hosting lease ended {abs(days_left)} days ago!'


def get_work_urls():
    html = requests.get(
        'https://docs.google.com/spreadsheets/d/e/2PACX-1vTpz65FVwIho9EHlat1BtzNoG-dihl4ALfrgpzfcS0qh0gavt7IOBzgglji49g0RTwNs2wg1yELNIrX/pubhtml?gid=0&single=true').text
    soup = BeautifulSoup(html, "html.parser")
    tables = soup.find_all("table")

    data = []
    for table in tables:
        data.append([[td.text for td in row.find_all("td")] for row in table.find_all("tr")])
    data = data[0][1:]
    urls = [d[0] for d in data]
    urls = [url for url in urls if url]
    # [print(repr(url)) for url in urls]
    # urls = urls[:200]
    return urls


def parse_url(url):
    driver = get_driver()
    try:
        # print("Loading next URL")
        # # disable images start =================
        # chrome_options = webdriver.ChromeOptions()
        # prefs = {"profile.managed_default_content_settings.images": 2}
        # chrome_options.add_experimental_option("prefs", prefs)
        # driver = webdriver.Chrome(chrome_options=chrome_options)
        # # disable images end ====================

        logger.info("Loading URL: %s", url)
        driver.get(url)
        wait = WebDriverWait(driver, 10)
        t = wait.until(EC.visibility_of_element_located((By.CLASS_NAME, 'orders')))
        quantity = t.text.split()[0]
        t = wait.until(EC.visibility_of_element_located((By.CLASS_NAME, 'new-price')))
        price = t.text.split()[0]

        return [url, quantity, price]
    finally:
        try:
            driver.close()
            driver.quit()
        except WebDriverException:
            logger.exception("Closing failed")

        gc.collect()


def parse_urls(work_urls, filename, resume=False):
    """
    Run the parsing job.
    work_urls - The list of URLs to be parsed.
    filename - The string used as a base for the output file path.
    result - If set to True, the function will reload existing output from
        the output file and will append to it instead of overwriting it.
    """
    if resume:
        with open(get_save_path(filename)) as f:
            out = json.load(f)['data']
    else:
        out = [[days_left_info, '', '']]

    count = -1
    for url in work_urls:
        count += 1

        retries = 0
        success = False
        while retries < 10:
            retries += 1
            try:
                log_memory_usage()

                url, quantity, price = parse_url(url)
                print(f"{len(work_urls)-1}-{count}", [url, quantity, price])
                out.append([url, quantity, price])
                success = True

                log_memory_usage()
                break
            except Exception:
                logger.exception("Error while loading URL")
                time.sleep(60)

        if not success:
            out.append([url, 'The URL could not be parsed', ''])

        if days_left < 0:
            out = out[0]
        out[0][2] = f' and was ended at {datetime.now().time()}'
        with open(get_save_path(filename), 'w') as f:
            json.dump({'data': out}, f)


def should_restart_parsing(filename):
    """
    Returns True if the script should start parsing the URLs from scratch at this day.
    """
    is_monday = date.today().weekday() == 0  # Monday
    output_file_exists = os.path.exists(get_save_path(filename))

    return is_monday or not output_file_exists


def get_parsed_urls(filename) -> List[str]:
    """
    Returns the list of successfully parsed URLs from the output file.
    """
    with open(get_save_path(filename)) as f:
        output = json.load(f)

    url_items = output['data'][1:]
    urls = [item[0] for item in url_items]

    return urls


def run(filename, **kwargs):
    # selenium.common.exceptions.InvalidArgumentException:
    # driver.get("https:::google.com")

    # selenium.common.exceptions.WebDriverException: Message: unknown error: net::ERR_NAME_NOT_RESOLVED
    # driver.get("https://googleeee.com")

    # 404 - no exception
    # driver.get("https://google.com/eeee")

    # Есть временный файл?
    # Да
    #   Работает ли процесс с ID, записанным в файл?
    #   Да
    #       Пропускаем запуск
    #   Нет
    #       Запускаем с последнего URL, записанного в JSON
    #       Перезаписываем новый PID во временный файл
    # Нет
    #    Предыдущий запуск завершился успешно
    #    Парсим URL заново

    status = get_last_run_status(__name__)

    # If this script is still running - don't run it againt
    if status == RunStatus.STILL_RUNNING:
        logger.info("This script is still running. Skipping repeated run.")
        return
    elif status == RunStatus.FINISHED_OK:
        logger.info("The script has finished OK last time.")
        if should_restart_parsing(filename):
            logger.info("Restarting the parsing.")

            update_pid_file(__name__)

            work_urls = get_work_urls()
            logger.info("URLs in the work sheet: %s", len(work_urls))

            parse_urls(work_urls, filename)

            delete_pid_file(__name__)

        else:
            logger.info("Skipping the parsing for now. (should_restart_parsing returned False)")
    elif status == RunStatus.ERRORED:
        logger.info("The script has errored last time. Resuming the parsing.")

        update_pid_file(__name__)

        parsed_urls = get_parsed_urls(filename)
        logger.info("URLs parsed successfully at this point: %s", len(parsed_urls))

        work_urls = get_work_urls()
        logger.info("URLs in the work sheet: %s", len(work_urls))

        unparsed_urls = [url for url in work_urls if url not in parsed_urls]
        logger.info("URLs yet unparsed: %s", len(unparsed_urls))

        parse_urls(unparsed_urls, filename, resume=True)

        delete_pid_file(__name__)
