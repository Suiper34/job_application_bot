import os
from time import sleep

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.ui import WebDriverWait

options = webdriver.ChromeOptions().add_experimental_option('detach', True)
job_driver = webdriver.Chrome(options=options)

job_driver.get('https://www.linkedin.com/jobs/')

username = WebDriverWait(job_driver, 30).until(
    expected_conditions.presence_of_element_located((By.NAME, 'session_key'))
)
username.send_keys(os.environ.get('username'), Keys.ENTER)

password = WebDriverWait(job_driver, 30).until(
    expected_conditions.presence_of_element_located(
        (By.NAME, 'session_password'))
)
password.send_keys(os.environ.get('password'), Keys.ENTER)

search_job = WebDriverWait(job_driver, 20).until(
    expected_conditions.presence_of_element_located((By.CSS_SELECTOR, 'input[aria-label="Search by title, skill, or company"]')))
search_job.send_keys('Python Developer', Keys.ENTER)


filter_select = WebDriverWait(job_driver, 20).until(
    expected_conditions.element_to_be_clickable(
        (By.CSS_SELECTOR, '.relative.mr2 button'))
)
filter_select.click()


easy_apply = WebDriverWait(job_driver, 5).until(
    expected_conditions.presence_of_element_located(
        (By.XPATH, "//li[contains(@class, 'search-reusables__secondary-filters-filter')][.//h3[contains(text(), 'Easy Apply')]]//input[@type='checkbox' and contains(@class, 'artdeco-toggle__button')]")
    )
)
if easy_apply.get_attribute('aria-checked') != 'true':
    easy_apply.click()


apply_filter = WebDriverWait(job_driver, 2).until(
    expected_conditions.element_to_be_clickable((By.CSS_SELECTOR, '.artdeco-modal-overlay.search-reusables__side-panel-overlay button[aria-label ="Apply current filters to show results"]')))

sleep(5)
job_results = job_driver.find_elements(
    By.CSS_SELECTOR, 'a.job-card-list__title')

for job in job_results:
    job.click()

    apply_job = WebDriverWait(job_driver, 4).until(
        expected_conditions.element_to_be_clickable((By.ID, 'jobs-apply-button-id')))
    apply_job.click()

    enter_number = WebDriverWait(job_driver, 15).until(expected_conditions.presence_of_element_located(
        (By.ID, 'single-line-text-form-component-formElement-urn-li-jobs-applyformcommon-easyApplyFormElement-4254357231-14023255337-phoneNumber-nationalNumber')))
    enter_number.send_keys(os.environ.get('number'))

    sleep(1)

    next_button = job_driver.find_element(
        By.CSS_SELECTOR, '.jobs-easy-apply-modal__content button[aria-label="Continue to next step"]'
    )
    next_button.click()

    the_button = job_driver.find_element(
        By.CSS_SELECTOR, '.jobs-easy-apply-modal__content button')
    if the_button.get_attribute('aria-label') == 'Continue to next step':
        sleep(5)
        next_button.click()

    elif the_button.get_attribute('aria-label') == 'Review your application':
        review_button = WebDriverWait(job_driver, 5).until(expected_conditions.element_to_be_clickable(
            (By.CSS_SELECTOR, '.jobs-easy-apply-modal__content button[aria-label = "Review your application"]')))
        review_button.click()
    else:
        sleep(10)
        submit_button = job_driver.find_element(
            By.CSS_SELECTOR, '.jobs-easy-apply-modal__content button[aria-label = "Submit application"]')
        submit_button.click()
