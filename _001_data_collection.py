"""
The module responsible for creating RAW data format,
from queries from defined:
    - job title
    - number of offers
Additional parameters are:
    - driver's path for selected web browser
    - debug mode for development and debugging
Arguments could be passed from the global config data file or directly into the function.
"""
# Python
import random
from typing import Any, Union
import time

# External
from selenium import webdriver
from selenium.common.exceptions import (
    NoSuchElementException, ElementClickInterceptedException, WebDriverException, TimeoutException, NoSuchElementException)
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
import requests
# import pandas as pd

# Internal
from config.get import get_config, get_url
from _types import DriverChrome

config = get_config()
JobsList = list[Union[dict[str, Any], None]]


def get_df_job_postings(
        job_title: str = config["jobs_titles"]["default"],
        jobs_number: int = config["jobs_number"],
        driver_path: str = config["driver_path"],  # todo
        debug_mode: bool = config["debug_mode"]
):
    """returns DataFrame object from searched phrase on glassdoor.com"""

    url = get_url(config['url'], job_title)
    driver = get_webpage(url, debug_mode)
    jobs_rows: JobsList = []

    while len(jobs_rows) < jobs_number:

        jobs_list_buttons = await_element(
            driver, 15, By.XPATH, '//ul[@data-test="jlGrid"]')

        jobs_buttons = jobs_list_buttons.find_elements(
            By.TAG_NAME, "li")

        click_x_pop_up(driver)

        NA_value = -1

        for job_button in jobs_buttons:

            print("Progress: {}".format(
                "" + str(len(jobs_rows) + 1) + "/" + str(jobs_number)))
            if len(jobs_rows) >= jobs_number:
                break

            pause_for_bot_detection()

            job_button.click()

            job_column = await_element(
                driver, 10, By.ID, 'JDCol')

            click_x_pop_up(driver)

            job_description = {
                "Company_Name": {"value": NA_value, "element": './/div[@data-test="employerName"]'},
                "Rating": {"value": NA_value, "element": './/span[@data-test="detailRating"]'},
                "Location":  {"value": NA_value, "element": './/div[@data-test="location"]'},
                "Job_Title":  {"value": NA_value, "element": './/div[@data-test="jobTitle"]'},
                "Description":  {"value": NA_value, "element": './/div[@class="jobDescriptionContent desc"]'},
                "Salary":  {"value": NA_value, "element": './/span[@data-test="detailSalary"]'},
                "Apply_Type":  {"value": NA_value, "element": './/button[@data-test="applyButton"]'},

            }

            job_description = get_values(job_column, job_description)

            job_button_info = {
                "Job_Age": {"value": NA_value, "element": './/div[@data-test="job-age"]'},
            }

            job_button_info = get_values(job_button, job_button_info)

            company_description = {
                "Size": {'value': NA_value, "element": './/div//*[text() = "Size"]//following-sibling::*'},
                "Type_of_ownership": {'value': NA_value, "element": './/div//*[text() = "Type"]//following-sibling::*'},
                "Sector": {'value': NA_value, "element": './/div//*[text() = "Sector"]//following-sibling::*'},
                "Founded": {'value': NA_value, "element": './/div//*[text() = "Founded"]//following-sibling::*'},
                "Industry": {'value': NA_value, "element": './/div//*[text() = "Industry"]//following-sibling::*'},
                "Revenue": {'value': NA_value, "element": './/div//*[text() = "Revenue"]//following-sibling::*'},
            }

            try:
                company_info = job_column.find_element(By.ID, "EmpBasicInfo")
                company_description = get_values(
                    company_info, company_description)

            except NoSuchElementException:
                pass

            # rating_description = {
            #     "Company_Name": {"value": NA_value, "element": './/div[@data-test="employerName"]'},
            # }

            try:
                rating_info = job_column.find_element(
                    By.XPATH, '//div[@data-test="company-ratings"]')
                # company_description = get_values(
                #     rating_info, rating_description)

                print("rating_info", rating_info)
            except NoSuchElementException as E:
                print("error:\n", E)
                pass

            # rating_description = get_values(job_column, job_description)

            # if debug_mode:
            #     print_key_value_pairs(job_description)
            #     print_key_value_pairs(job_button_info)
            #     print_key_value_pairs(company_description)
            #     print("@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@")


def pause_for_bot_detection():
    random_sleep = random.uniform(0.5, 1.4)
    time.sleep(random_sleep)


def get_values(source_html, job_values):

    for values in job_values.values():
        try:
            values['value'] = get_XPATH_element(
                source_html, values['element'])
        except NoSuchElementException:
            pass

    return job_values


def get_XPATH_element(source_html, element):
    return source_html.find_element(
        By.XPATH, element
    ).text


def print_key_value_pairs(values):
    for key, value in values.items():
        v = value['value']
        v = v[:500] if type(v) is str else v
        print(f"{key}: {v}")


def get_employer_info(source_html, category):
    return source_html.find_element(
        By.XPATH, f'.//div//*[text() = "{category}"]//following-sibling::*'
    ).text


def await_element(driver, time, by, elem):
    return WebDriverWait(driver, time).until(
        lambda x: x.find_element(by, elem))

    """pass blocking pop-ups"""

    rid_off_sign_up(driver)

    # to simulate human behavior for bot detection
    time.sleep(.1)

    click_x_pop_up(driver)


def click_x_pop_up(driver):
    """pass pop-up"""

    try:
        x_button = await_element(
            driver, 3, By.CSS_SELECTOR, '[alt="Close"]')
        x_button.click()
    except (NoSuchElementException, TimeoutException):
        pass


def rid_off_sign_up(driver):
    """pass pop-up"""

    try:
        driver.find_element(By.CLASS_NAME, "selected").click()
    except (ElementClickInterceptedException, NoSuchElementException):
        pass


def get_webpage(url, debug_mode):
    """returns browser driver"""

    driver: DriverChrome = get_driver(debug_mode)
    try:
        driver.get(url)
    except WebDriverException as error:
        status_code = requests.get(url, timeout=3).status_code
        print(
            f"Failed to upload the url: {error}\n Status code: {status_code}")

    return driver


def get_driver(
        debug_mode: bool = config["debug_mode"],
        path: str = config["driver_path"]) -> DriverChrome:
    """returns website driver with custom options"""

    options = webdriver.ChromeOptions()

    # to simulate human behavior for bot detection
    options.add_argument("USER AGENT")

    if not debug_mode:
        options.add_argument('headless')

    # Change the path to where chromedriver/other browser is if you need to.
    driver = webdriver.Chrome(
        executable_path=path, options=options)
    # driver.set_window_rect(width=1120, height=1000)
    return driver


if __name__ == "__main__":

    get_df_job_postings(debug_mode=True)  # test todo
