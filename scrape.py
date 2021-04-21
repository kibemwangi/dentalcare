import logging
import time
import pandas as pd
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import WebDriverException
from selenium.common.exceptions import TimeoutException
import requests


class DentalCare():

    def __init__(self):
        self.complete_df = pd.DataFrame(columns=["Hospital_name", "Treatment_type", "Price", "Discount"])
        self.complete_global_hospital_names = []
        self.complete_global_treatment_types = []
        #self.complete_global_doctors = []
        self.complete_global_prices = []
        self.complete_global_discounts = []
        self.driver = self.start_driver()

    def start_driver(self):
        chrome_options = webdriver.ChromeOptions()
        # chrome_options.add_argument('--headless')
        driver = webdriver.Chrome(
            executable_path="./chromedriver", options=chrome_options)
        driver.maximize_window()
        return driver

    def site(self):

        self.driver.get(
            'https://saudi.vezeeta.com/en/offers/dental-care')
        time.sleep(2)
        global_hospital_names = []
        global_treatment_types = []
        # global_doctors = []
        global_prices = []
        global_discounts = []
        # open individual treatment

       

        elements = self.driver.find_elements_by_css_selector(
            'div.OfferItemBigstyle__ItemContent-sc-1t2pm83-11.geEdgE')

        for i, element in enumerate(elements):
            time.sleep(2)
            elements[i].click()
            time.sleep(2)

            # get hospitals name
            hospital_names = self.driver.find_elements_by_css_selector(
                'p.BundleProfileComstyle__EntityName-sc-6maffe-64.bypjky')
            hospital_names_ = [hospital_name.text for hospital_name in hospital_names]

            # get treatment type
            treatment_types = self.driver.find_elements_by_css_selector(
                'div.BundleProfileComstyle__BundleName-sc-6maffe-9.kGIugI')
            treatment_types_ = [treatment_type.text for treatment_type in treatment_types]

            # get doctors name
            # doctors = self.driver.find_elements_by_css_selector(
            #     'p.DoctorsCarouselstyle__DrName-xq5jy1-5.eecTVM, p.DoctorsCarouselstyle__DrName-xq5jy1-5.eecTVM, p.DoctorsCarouselstyle__DrName-xq5jy1-5.eecTVM, p.DoctorsCarouselstyle__DrName-xq5jy1-5.eecTVM')
            # doctors_ = [doctor.text for doctor in doctors]

            # get prices after discount
            prices = self.driver.find_elements_by_css_selector(
                'span.BundleProfileComstyle__PriceAfter-sc-6maffe-16.cNNDjW')
            prices_ = [price.text for price in prices]

            #discount offered
            discounts = self.driver.find_elements_by_css_selector(
                'span.BundleProfileComstyle__SpanSaved-sc-6maffe-62.bomHNs')
            discounts_ = [discount.text for discount in discounts]

            global_hospital_names.extend(hospital_names_)
            global_treatment_types.extend(treatment_types_)
            # global_doctors.extend(doctors_)
            global_prices.extend(prices_)
            global_discounts.extend(discounts_)

            self.complete_global_hospital_names.extend(hospital_names_)
            self.complete_global_treatment_types.extend(treatment_types_)
            # self.complete_global_doctors.extend(doctors_)
            self.complete_global_prices.extend(prices_)
            self.complete_global_discounts.extend(discounts_)
            time.sleep(2)
            self.driver.execute_script("window.history.go(-1)")
                

            if i > 1 and i % 10 == 0 :
                self.df = pd.DataFrame(columns=["Hospital_name", "Treatment_type", "Doctor", "Price", "Discount"])
                self.df["Hospital_name"] = global_hospital_names
                self.df["Treatment_type"] = global_treatment_types
                # self.df["Doctors"] = global_doctors
                self.df["Price"] = global_prices
                self.df["Discount"] = global_discounts
                self.df.to_csv(f'output_{i}.csv', index=False)
                global_hospital_names = []
                global_treatment_types = []
                # global_doctors = []
                global_prices = []
                global_discounts = []


            for hospital_name, treatment_type, price, discount in zip(hospital_names_, treatment_types_, prices_, discounts_):
                print(f"{hospital_name} >>>>>>>>> {treatment_type} >>>>>>>> {price} >>>>>>> {discount}")
                
            elements = self.driver.find_elements_by_css_selector('div.OfferItemBigstyle__ItemContent-sc-1t2pm83-11.geEdgE')
        time.sleep(2)

    def next_page(self):
        tries = 0
        while tries < 21:
            try:
                time.sleep(3)
                self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                next_button = self.driver.find_element_by_xpath(
                    '//*[@id="OffersGetChildKey__Pagination-page--next"]')
                ActionChains(self.driver).move_to_element(
                    next_button).click().perform()
                tries += 1
            except Exception as e:
                logging.error(f'No Next button found due to error {e}...')

    def write_final_file(self):
        self.complete_df["Hospital_name"] = self.complete_global_hospital_names
        self.complete_df["Treatment_type"] = self.complete_global_treatment_types
        # self.complete_df["Doctor"] = self.complete_global_doctors
        self.complete_df["Price"] = self.complete_global_prices
        self.complete_df["Discount"] = self.complete_global_discounts

        self.complete_df.to_csv('output_final.csv', index=False)

    def run(self):
        try:
            self.site()
        except Exception as e:
            print('Scraper interupted', e)
        finally:
            self.write_final_file()


DentalCare().run()
