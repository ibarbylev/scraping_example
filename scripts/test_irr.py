import time
# https://selenium-python.readthedocs.io/
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By



driver = webdriver.Chrome()

try:
    driver.get('https://irr.ru/')

    button = driver.find_element_by_css_selector('.js-authorizationButton')
    button.click()

    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, ".ReactModal__Content")),
    )

    email_input = driver.find_element_by_css_selector('.ReactModal__Content [name="email"]')
    email_input.send_keys("it4each.com@gmail.com")

    password_input = driver.find_element_by_css_selector('.ReactModal__Content [name="password"]')
    password_input.send_keys("Aasdf1")

    button = driver.find_element_by_css_selector('.ReactModal__Content button[type=submit]')
    button.click()

    time.sleep(20)
finally:
    driver.close()

