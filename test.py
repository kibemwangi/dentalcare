# importing necessary packages
import xlsxwriter
import pandas as pd

from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
  
# for holding the resultant list
element_list = []

for page in range(1, 3, 1):
    page_url = 'https://saudi.vezeeta.com/en/doctor/all-specialities/saudi-arabia?page=' + str(page)
    
    driver = webdriver.Chrome(ChromeDriverManager().install())
    driver.get(page_url)
    driver.maximize_window()
    doctors_name = driver.find_elements_by_xpath('//*/span/div/div[2]/a/span')
    locations = driver.find_elements_by_xpath('//*/span/div/div[2]/span[2]/span[4]')
    

    for i in range(len(doctors_name)):
        element_list.append([doctors_name[i].text, locations[i].text])

with xlsxwriter.Workbook('Doctors and Locations.xls') as workbook:
    worksheet = workbook.add_worksheet()
  
    for row_num, data in enumerate(element_list):
        worksheet.write_row(row_num, 0, data)

print(element_list)

driver.close