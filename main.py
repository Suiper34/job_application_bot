import os
from time import sleep

from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.ui import WebDriverWait

options = webdriver.ChromeOptions().add_experimental_option('detach', True)
job_driver = webdriver.Chrome(options=options)

job_driver.get('https://www.linkedin.com/jobs/')

# sign in if login pages exist
try:
    username = WebDriverWait(job_driver, 30).until(
        expected_conditions.presence_of_element_located(
            (By.NAME, 'session_key'))
    )
    username.send_keys(os.environ.get('username'), Keys.ENTER)

    password = WebDriverWait(job_driver, 2).until(
        expected_conditions.presence_of_element_located(
            (By.NAME, 'session_password'))
    )
    password.send_keys(os.environ.get('password'), Keys.ENTER)

except Exception as e:
    print('Login form not found or login failed. Exception:', e)

# wait 20 secs and pass in job title to search for job
search_job = WebDriverWait(job_driver, 20).until(
    expected_conditions.presence_of_element_located((By.CSS_SELECTOR, 'input[aria-label="Search by title, skill, or company"]')))
search_job.send_keys('Python Developer', Keys.ENTER)

# find filter and click on it after 20secs
filter_select = WebDriverWait(job_driver, 20).until(
    expected_conditions.element_to_be_clickable(
        (By.CSS_SELECTOR, '.relative.mr2 button'))
)
filter_select.click()

# turn on easy apply if off
easy_apply = WebDriverWait(job_driver, 5).until(
    expected_conditions.presence_of_element_located(
        (By.XPATH, "//li[contains(@class, 'search-reusables__secondary-filters-filter')][.//h3[contains(text(), 'Easy Apply')]]//input[@type='checkbox' and contains(@class, 'artdeco-toggle__button')]")
    )
)
if easy_apply.get_attribute('aria-checked') != 'true':
    easy_apply.click()

# apply filter to show easy apply jobs
apply_filter = WebDriverWait(job_driver, 2).until(
    expected_conditions.element_to_be_clickable((By.CSS_SELECTOR, '.artdeco-modal-overlay.search-reusables__side-panel-overlay button[aria-label ="Apply current filters to show results"]')))

# easy apply job results
sleep(7)
job_results = job_driver.find_elements(
    By.CSS_SELECTOR, 'a.job-card-list__title')

for job in job_results:
    job.click()

    apply_job = WebDriverWait(job_driver, 4).until(
        expected_conditions.element_to_be_clickable((By.ID, 'jobs-apply-button-id')))
    apply_job.click()  # click on apply button

    enter_number = WebDriverWait(job_driver, 15).until(expected_conditions.presence_of_element_located(
        (By.ID, 'single-line-text-form-component-formElement-urn-li-jobs-applyformcommon-easyApplyFormElement-4254357231-14023255337-phoneNumber-nationalNumber')))
    enter_number.send_keys(os.environ.get('number'))  # input phone number

    sleep(1)

    while True:
        try:
            next_button = WebDriverWait(job_driver, 3).until(
                expected_conditions.element_to_be_clickable(
                    (By.CSS_SELECTOR,
                     '.jobs-easy-apply-modal__content button[aria-label="Continue to next step"]')
                )
            )
            next_button.click()
            sleep(1)

            # assume error if the next button is still present and clickable,
            still_next = job_driver.find_elements(
                By.CSS_SELECTOR, '.jobs-easy-apply-modal__content button[aria-label="Continue to next step"]')
            if still_next:
                print(
                    'Next button still present, likely missing required field.')
                break

        except TimeoutException:
            break  # exit loop if no more next buttons

    # click review button if present
    try:
        review_button = WebDriverWait(job_driver, 5).until(
            expected_conditions.element_to_be_clickable(
                (By.CSS_SELECTOR,
                 '.jobs-easy-apply-modal__content button[aria-label="Review your application"]')
            )
        )
        review_button.click()
        sleep(1)
    except TimeoutException:
        pass  # continue review button not present

    # click submit button if present
    try:
        submit_button = WebDriverWait(job_driver, 8).until(
            expected_conditions.element_to_be_clickable(
                (By.CSS_SELECTOR,
                 '.jobs-easy-apply-modal__content button[aria-label="Submit application"]')
            )
        )
        submit_button.click()

    except TimeoutException:
        print('Submit button not found.')
