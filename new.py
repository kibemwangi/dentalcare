import yaml
import logging
import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.action_chains import ActionChains
import csv 

class SoberNation():

    def __init__(self):
        self.driver = self.start_driver()
        self.site()
        self.variables = self.get_site_variables()
        self.county_data = self.variables['county_data']
        self.all_scraped_data = []
        self.all_columns = []

    def start_driver(self):
        chromeOptions = webdriver.ChromeOptions()
        driver = webdriver.Chrome(
            options=chromeOptions)
        driver.maximize_window()
        return driver

    def get_site_variables(self):
        variables_file = './variables.yaml'
        logging.info(f'Loading variables from {variables_file}...')
        try:
            with open(variables_file, 'r') as file:
                variables = yaml.load(file, Loader=yaml.FullLoader)
        except Exception as e:
            logging.error(
                'File not found...')
            raise
        return variables


    def site(self):

        # df = pd.read_excel(r'urls.xlsx')
        # url = df['urls'].tolist()
        
        self.driver.get(
            'https://sobernation.com/rehab/new-york/')
            
        time.sleep(2)
        self.driver.find_element_by_css_selector('a.county').click()

    def write_csv(self, data):
        csv_columns = []
        for data in self.county_data:
            csv_columns.extend(
                self.variables['county_data']['fieldnames'])
        with open('./data.csv', 'w') as f:
            writer = csv.DictWriter(f, fieldnames=csv_columns)
            writer.writeheader()
            for county_data in data:
                writer.writerow(county_data)
        names = self.driver.find_elements_by_css_selector('h4')
        for name in names:
            print(name.text)
        time.sleep(2)
        
        addresses = self.driver.find_elements_by_css_selector('div.address')
        for address in addresses:
            print(address.text)
        time.sleep(2)

SoberNation()