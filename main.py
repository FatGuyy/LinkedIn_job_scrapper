import os 
from logging import exception
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
import pandas as pd
import openpyxl


# Username and Password

#----------------------------------

USERNAME = ""
PASSWORD = ""

#----------------------------------

# Path to the Chromedriver

os.environ['PATH'] += r'.\chromedriver.chromedriver.exe'
driver = webdriver.Chrome()
driver.set_window_size(1024,600)
driver.maximize_window()

# get the website
driver.get("https://www.linkedin.com/login?fromSignIn=true&trk=guest_homepage-basic_nav-header-signin")
driver.implicitly_wait(30)

# login functionality
try:
    username = driver.find_element(by=By.ID, value='username')
    username.send_keys(USERNAME)
    password = driver.find_element(by=By.ID, value='password')
    password.send_keys(PASSWORD)
    Login = driver.find_element(by=By.XPATH, value="/html/body/div/main/div[2]/div[1]/form/div[3]/button")
    Login.click()
    driver.implicitly_wait(30)
except exception as e:
    print('Unable to login')
    

# Searching functionality
try:
    Keyword1 = "Product"
    Keyword2 = "Engineer"
    # declare more keyword if needed

    URL = "https://www.linkedin.com/jobs/"
    driver.get(URL)
    
    search_bars = driver.find_element(by=By.CLASS_NAME, value='jobs-search-box__text-input')
    search_bars.click()
    
    search_bars.send_keys(Keyword1)
    time.sleep(1)
    
    search_bars.send_keys(Keys.SPACE)
    time.sleep(1)
    
    search_bars.send_keys(Keyword2)
    time.sleep(1)
    
    search_bars.send_keys(Keys.ENTER)
    
except exception as e:
    print("unable to search")

# Create a Dictionary to store the job title as 
jobs_dict = {}

# Scraping the data
try:
    # Every search in Jobs returns 40 pages of results
    # range(1, 41)
    for i in range(1, 41):
        # click button to change the job list(page)
        driver.find_element(By.XPATH, value=f'//button[@aria-label="Page {i}"]').click()
        time.sleep(2)



        # Usually each page shows 25 results but this may change resulting in error.
        # Therefore a variable(s) is declared which is used to find the length of the list
        # then iterate through the list using the length as the range.
        
        jobs_lists = driver.find_element(By.CLASS_NAME,
            value='scaffold-layout__list-container')  # create a list with jobs

        jobs = jobs_lists.find_elements(By.CLASS_NAME,
            value='jobs-search-results__list-item')  # select each job to count

        #   wait for loading
        driver.implicitly_wait(30)

        for job in range(1, len(jobs)+1):
            
            # job click
            driver.find_element(by=By.XPATH, value=f'/html/body/div[5]/div[3]/div[4]/div/div/main/div/section[1]/div/ul/li[{job}]').click()
            driver.implicitly_wait(20)
            
            # # get the job title
            titles = driver.find_element(by=By.XPATH, value=f'/html/body/div[5]/div[3]/div[4]/div/div/main/div/section[1]/div/ul/li[{job}]/div/div[1]/div[1]/div[2]/div[1]/a').text
            # # get the job Link
            links = driver.find_element(by=By.XPATH, value=f'/html/body/div[5]/div[3]/div[4]/div/div/main/div/section[1]/div/ul/li[{job}]/div/div[1]/div[1]/div[2]/div[1]/a').get_attribute("href")
            # # wait  
            driver.implicitly_wait(5)
            
            # store the data in the dictionary
            jobs_dict.update({titles:links})
            
except exception as e:
    print("Unable to scrape")

# export the dictionary to a csv file

try:
    df = pd.DataFrame(jobs_dict, index=["Links"])
    df = (df.T)
    df.to_excel('listing.xlsx')
    
except exception as e:
    print('Unable to export')

driver.close()