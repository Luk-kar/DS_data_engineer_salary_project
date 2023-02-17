'''
This module contains a function that tries to locate a pop-up close button on a web page 
and clicks it, thus preventing the pop-up from blocking the drivers's access.
'''
# External
from selenium.common.exceptions import (
    TimeoutException,
    NoSuchElementException
)
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.webdriver import WebDriver

# Internal
from scraper._types import WebElem
from scraper.helpers.await_element import await_element


def click_x_pop_up(driver: WebElem | WebDriver):
    """Riding off pop-up blocking web page elements"""

    try:
        x_button = await_element(
            driver, 3, By.CSS_SELECTOR, '[alt="Close"]')
        x_button.click()

    except (NoSuchElementException, TimeoutException):
        pass
