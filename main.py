from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

options = webdriver.ChromeOptions.add_experimental_option('detach', True)
job_driver = webdriver.Chrome(options=options)
