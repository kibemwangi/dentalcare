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

# driver = webdriver.Chrome(ChromeDriverManager().install())

class DentalCare():

    def __init__(self):
        self.complete_df = pd.DataFrame(columns=[
            "Doctor_name", "Job_description", "Specialisation", "Location", "Charges", "Waiting_time", "Contact", "Hospital_name"])

        self.complete_global_doctor_names = []
        self.complete_global_job_descriptions = []
        self.complete_global_specialisations = []
        self.complete_global_locations = []
        self.complete_global_charges = []
        self.complete_global_waiting_times = []
        self.complete_global_contacts = []
        self.complete_global_hospital_names = []
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
            'https://saudi.vezeeta.com/en/doctor/')
        time.sleep(2)

        global_doctor_names = []
        global_job_descriptions = []
        global_specialisations = []
        global_locations = []
        global_charges = []
        global_waiting_times = []
        global_contacts = []
        global_hospital_names = []

        elements = self.driver.find_elements_by_xpath(
            '//*/div/div[1]/div[2]/div/div/div[2]/div/a[1]')

        time.sleep(2)
        # self.driver.execute_script("window.scrollTo(10, document.body.scrollHeight);")
        
        for i, element in enumerate(elements):
            time.sleep(2)
            elements[i].click()
            time.sleep(3)

            # get doctors name
            doctor_names = self.driver.find_elements_by_xpath(
                '//*/span/div/div[2]/a/span')
            doctor_names_ = [doctor_name.text for doctor_name in doctor_names]

            # get job description
            job_descriptions = self.driver.find_elements_by_xpath(
                '//*/span/div/div[2]/h3')
            job_descriptions_ = [
                job_description.text for job_description in job_descriptions]

            # get Specialisations data
            specialisations = self.driver.find_elements_by_xpath(
                '//*/span/div/div[2]/span[2]/span[2]/span/h3/a/span')
            specialisations_ = [specialisation.text for specialisation in specialisations]

            # Doctors Location
            locations = self.driver.find_elements_by_xpath('//*/span/div/div[2]/span[2]/span[4]')
            locations_ = [location.text for location in locations]

            # Doctors Charges
            charges = self.driver.find_elements_by_xpath(
                '//*/span/div/div[2]/span[2]/span[7]')
            charges_ = [charge.text for charge in charges]

            # Waiting Time
            waiting_times = self.driver.find_elements_by_xpath(
                '//*/span/div/div[2]/span[2]/span[9]')
            waiting_times_ = [waiting_time.text for waiting_time in waiting_times]


            # Doctors Contacts
            contacts = self.driver.find_elements_by_xpath(
                '//*/span/div/div[2]/span[2]/a/span')
            contacts_ = [contact.text for contact in contacts]

            # Hospitals Name
            hospital_names = self.driver.find_elements_by_xpath(
                '//*/span/a/span/span')
            hospital_names_ = [hospital_name.text for hospital_name in hospital_names]

            global_doctor_names.extend(doctor_names_)
            global_job_descriptions.extend(job_descriptions_)
            global_specialisations.extend(specialisations_)
            global_locations.extend(locations_)
            global_charges.extend(charges_)
            global_waiting_times.extend(waiting_times_)
            global_contacts.extend(contacts_)
            global_hospital_names.extend(hospital_names_)

            time.sleep(2)
            self.complete_global_doctor_names.extend(doctor_names_)
            self.complete_global_job_descriptions.extend(job_descriptions_)
            self.complete_global_specialisations.extend(specialisations_)
            self.complete_global_locations.extend(locations_)
            self.complete_global_charges.extend(charges_)
            self.complete_global_waiting_times.extend(waiting_times_)
            self.complete_global_contacts.extend(contacts_)
            self.complete_global_hospital_names.extend(hospital_names_)

            time.sleep(2)


            if i > 1 and i % 20 == 0 :
                self.df = pd.DataFrame(columns=["Doctor_name", "Specialisation",
                    "Location", "Charges", "Waiting_time", "Contact", "Hospital_name"])

                self.df["Doctor_name"] = global_doctor_names
                self.df["Job_description"] = global_job_descriptions
                self.df["Specialisation"] = global_specialisations
                self.df["Location"] = global_locations
                self.df["Charges"] = global_charges
                self.df["Waiting_time"] = global_waiting_times
                self.df["Contact"] = global_contacts
                self.df["Hospital_name"] = global_hospital_names

                self.df.to_csv(f'doctors_data_{i}.csv', index=False)
                global_doctor_names = []
                global_job_descriptions = []
                global_specialisations = []
                global_locations = []
                global_charges = []
                global_waiting_times = []
                global_contacts = []
                global_hospital_names = []


            for doctor_names, job_descriptions, specialisations, location, charges, waiting_times, contacts, hospitals_names in zip(doctor_names_
                , job_descriptions_, specialisations_, locations_, charges_, waiting_times_, contacts_, hospital_names_):
                print(f"{doctor_names} >>>>>>>>> {job_descriptions} >>>>>>>> {specialisations} >>>>>>> {locations} >>>>>>>>>>>>")
                
            time.sleep(2)

        time.sleep(3)

    def write_final_file(self):

        self.complete_df["Doctor_name"] = self.complete_global_doctor_names
        self.complete_df["Job_description"] = self.complete_global_job_descriptions
        self.complete_df["Specialisation"] = self.complete_global_specialisations
        self.complete_df["Location"] = self.complete_global_locations
        self.complete_df["Charges"] = self.complete_global_charges
        self.complete_df["Waiting_time"] = self.complete_global_waiting_times
        self.complete_df["Contact"] = self.complete_global_contacts
        self.complete_df["Hospital_name"] = self.complete_global_hospital_names
        # self.complete_df["Doctor"] = self.complete_global_doctors
        

        self.complete_df.to_csv('doctors_data_final.csv', index=False)

    def run(self):
        try:
            self.site()
        except Exception as e:
            print('Scraper interupted', e)
        finally:
            self.write_final_file()


DentalCare().run()
