import os

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


job_results = job_driver.find_elements(
    By.CSS_SELECTOR, 'a.job-card-list__title')
