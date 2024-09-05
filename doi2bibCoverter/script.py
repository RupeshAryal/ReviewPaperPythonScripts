from selenium.webdriver import Chrome
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import time
import pandas as pd
import numpy as np


#function to verify if bibtex is correctly extracted
def verify_bibtex(text):
    if text[0] == '@':
        return True
    else:
        return False


#function to write bib text to a file 
def write_to_bib_file(text):
    with open('assets/reference.bib', 'a') as f:
        f.write('\n')
        f.write(text)


# sometime the website can throw error when many requests are made in a short time. We have to handle that
def handle_website_overload(text):
    if text != 'Too many requests, please try again later.':
        return False
    else:
        # time.sleep(5)
        return True


# loading the excel file containing doi and getting the list of all doi
doi_file =  pd.read_excel('../assets/doi_file.xlsx', sheet_name=['with Abstract'])
df = doi_file['with Abstract']
doi_column = df['Doi']
doi_list = list(doi_column)


# Browser Automation
driver = Chrome()
url = 'https://www.doi2bib.org/'

search_bar_xpath = '/html/body/div/div/div/div/div[3]/div/form/div/input'
get_button_xpath = '/html/body/div/div/div/div/div[3]/div/form/div/span/button'



bibtex = []
driver.get(url)

search_bar = driver.find_element(By.XPATH, search_bar_xpath)
get_button = driver.find_element(By.XPATH, get_button_xpath)

for doi in doi_list:
    
    #clears the search bar, inserts the doi and makes a request
    search_bar.clear()
    search_bar.send_keys(str(doi).strip())
    get_button.click()
    bibtex_area_xpath = '/html/body/div/div/div/div/div[4]/div/pre'

    #scraping bibtext from the response
    bibtex_area = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.XPATH, bibtex_area_xpath))
    )
    bibtex_area_text = bibtex_area.text
    too_many_requests = handle_website_overload(bibtex_area_text)


    #handling multiple requests error/ Usually the cooldown is 2/3 seconds. We have used 5 second for absolute measures
    if too_many_requests:
        time.sleep(5)
        search_bar.clear()
        search_bar.send_keys(str(doi).strip())
        get_button.click()
        bibtex_area_xpath = '/html/body/div/div/div/div/div[4]/div/pre'
        bibtex_area = WebDriverWait(driver, 10).until(
          EC.visibility_of_element_located((By.XPATH, bibtex_area_xpath))
        )


    #bibtex verification and appending bib text to bibliographic file
    if verify_bibtex(bibtex_area_text):
        bibtex.append(bibtex_area_text)
        write_to_bib_file(bibtex_area_text)

    else:
        bibtex.append(np.nan)
        write_to_bib_file(' ')

    
#final steps, creating a column in the original dataframe and exporting the df as a new excel file
driver.close()
df['bibtex'] = bibtex
df.to_excel('bibtex_included.xlsx')






