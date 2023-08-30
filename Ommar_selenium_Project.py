from random import random
from selenium import webdriver
import time
from pandas import DataFrame
import csv

from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException
from selenium.webdriver.common import by
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.wait import WebDriverWait

data = DataFrame(columns=['address','recommendations','rating', 'Valid until'])
filename = r'C:\Users\FARJAD\OneDrive\Desktop\Postal_Code_LE5_BATCH01.csv'
# initializing the titles and rows list
field = []
rows = []
#reading csv file
with open(filename, 'r') as csvfile:
    # creating a csv reader object
    csvreader = csv.reader(csvfile)
    # extracting field names through first row
    field = next(csvreader)
    # extracting each data row one by one
    for row in csvreader:
        rows.append(row)

driver = webdriver.Chrome(executable_path=r'C:\Users\FARJAD\Downloads\chromedriver_win32\chromedriver.exe')
url = 'https://www.gov.uk/find-energy-certificate'
url_imp = 'https://find-energy-certificate.service.gov.uk/find-a-certificate/search-by-postcode?lang=en&property_type=domestic'
driver.get(url)

# time.sleep(4)
driver.find_element_by_xpath('//*[@id="get-started"]/a').click()
time.sleep(3)
driver.find_element_by_xpath('//*[@id="domestic"]').click()
driver.find_element_by_xpath('//*[@id="main-content"]/form/fieldset/button').click()
# for row in rows:
# time.sleep(2)
def wait_for_page_load():
    timer = 10
    start_time = time.time()
    page_state = None
    while page_state != 'complete':
        time.sleep(0.5)
        page_state = driver.execute_script('return document.readyState;')
        if time.time() - start_time > timer:
            raise Exception('Timeout :(')

new_links = []

driver.find_element_by_xpath('//*[@id="postcode"]').clear()
# driver.find_element_by_xpath('//*[@id="postcode"]').send_keys("SK2 5AT")
# driver.find_element_by_xpath('//*[@id="main-content"]/div/div/form/fieldset/button').click()

for row in rows:
    driver.find_element_by_xpath('//*[@id="postcode"]').clear()
    driver.find_element_by_xpath('//*[@id="postcode"]').send_keys(row)
    driver.find_element_by_xpath('//*[@id="main-content"]/div/div/form/fieldset/button').click()
    links = []

# finding elements in tables
    recommendation = ''
    if(driver.find_elements_by_css_selector('tbody[class = govuk-table__body]')):
        table_item = driver.find_elements_by_css_selector("a[class = 'govuk-link']")
        for hrefs in table_item:
            links.append(hrefs.get_attribute('href'))
            # updated_links = links[4:]
        for list in links:
            print(list)
            driver.get(list)
            wait_for_page_load()
            if(driver.find_elements_by_xpath("//*[contains(text(), 'Change room heaters to condensing boiler')]") or
                driver.find_elements_by_xpath("//*[contains(text(), 'Replace boiler with new condensing boiler')]") or
                driver.find_elements_by_xpath("//*[contains(text(), 'Gas condensing boiler')]")):
                print('condition is okay')
                address = driver.find_element_by_css_selector("p[class = 'epc-address govuk-body']")
                print(address.text)
                date = driver.find_element_by_css_selector("p[class = 'govuk-body epc-extra-box']")
                print(date.text)
                rating = driver.find_element_by_css_selector("p[class = 'epc-rating-result govuk-body']")
                print(rating.text)
                data.to_csv(r'C:\Users\FARJAD\PycharmProjects\pythonProject\House_with_recommendation.csv')
                if(driver.find_elements_by_xpath("//*[contains(text(), 'Change room heaters to condensing boiler')]")):
                    recommendation = 'Change room heaters to condensing boiler'
                elif(driver.find_elements_by_xpath("//*[contains(text(), 'Replace boiler with new condensing boiler')]")):
                    recommendation = 'Replace boiler with new condensing boiler'
                elif(driver.find_elements_by_xpath("//*[contains(text(), 'Gas condensing boiler')]")):
                    recommendation = 'Gas condensing boiler'




                data.loc[-1] = [address.text, recommendation, rating.text, date.text]
                data.index = data.index + 1
                print(data)
            driver.back()
        driver.get(url)
        driver.find_element_by_xpath('//*[@id="get-started"]/a').click()
        time.sleep(3)
        driver.find_element_by_xpath('//*[@id="domestic"]').click()
        driver.find_element_by_xpath('//*[@id="main-content"]/form/fieldset/button').click()
    else:
        driver.back()
