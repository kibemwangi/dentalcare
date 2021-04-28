import logging
import time
import pandas as pd
from pandas import DataFrame
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import WebDriverException
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
import requests
from webdriver_manager.chrome import ChromeDriverManager

chrome_options = webdriver.ChromeOptions()
        # chrome_options.add_argument('--headless')
driver = webdriver.Chrome(
    executable_path="./chromedriver", options=chrome_options)
driver.maximize_window()

MAX_PAGE_NUM = 10
MAX_PAGE_DIG = 3

# with open('result.csv', 'w') as f:
#     f.write("Doctor_names, Job_descriptions, Specialisations, Locations, Charges, Waiting_times, Contacts, Hospital_names \n")

for i in range(1, MAX_PAGE_NUM + 1):
    page_num = (MAX_PAGE_DIG - len(str(i))) * "page=" + str(i)
    url = 'https://saudi.vezeeta.com/en/doctor/all-specialities/saudi-arabia?' + page_num

    driver.get(url)

    driver.maximize_window()

    doctor_names = driver.find_elements_by_xpath(
        '//*/span/div/div[2]/a/span')

    # get job description
    job_descriptions = driver.find_elements_by_xpath(
        '//*/span/div/div[2]/h3')

    # get Specialisations data
    specialisations = driver.find_elements_by_xpath(
        '//*/span/div/div[2]/span[2]/span[2]/span/h3/a/span')

    # Doctors Location
    locations = driver.find_elements_by_xpath('//*/span/div/div[2]/span[2]/span[4]')

    # Doctors Charges
    charges = driver.find_elements_by_xpath(
        '//*/span/div/div[2]/span[2]/span[7]')

    # Waiting Time
    waiting_times = driver.find_elements_by_xpath(
        '//*/span/div/div[2]/span[2]/span[9]')


    # Doctors Contacts
    contacts = driver.find_elements_by_xpath(
        '//*/span/div/div[2]/span[2]/a/span')

    # Hospitals Name
    hospital_names = driver.find_elements_by_xpath(
        '//*/span/a/span/span')

    num_page_items = len(doctor_names)
    with open('results.csv', 'a') as f:
        for i in range(num_page_items):
            f.write(doctor_names[i].text + ',' + job_descriptions[i].text + ',' + specialisations[i].text + ',' + locations[i].text + ',' + charges[i].text + ','
             + waiting_times[i].text + ',' + contacts[i].text + ',' + hospital_names[i].text + '\n')

driver.close()