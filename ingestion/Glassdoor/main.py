import time
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import pandas as pd
import pymongo
from io import StringIO
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Sleep for a few seconds to ensure the Selenium standalone server is ready
time.sleep(5)

# Set up Selenium ChromeOptions
options = webdriver.ChromeOptions()
options.add_argument("--headless")

# Initialize the WebDriver with the Selenium standalone server
driver = webdriver.Remote(
    command_executor='http://selenium:4444/wd/hub',
    options=options
)

# Navigate to Glassdoor
driver.get("https://www.glassdoor.com/")
driver.maximize_window()

# Enter your username and click to continue
username = WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.CSS_SELECTOR, "input[name='username']")))
username.clear()
username.send_keys('XXXXXXXXXXXX')
email_confirm = WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.CSS_SELECTOR, "button[type='submit']")))
email_confirm.click()

# Enter your password and click to login
password = WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.CSS_SELECTOR, "input[name='password']")))
password.clear()
password.send_keys('XXXXXXXXXXXX')
login = WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.CSS_SELECTOR, "button[type='submit']")))
login.click()

# Wait for 2 seconds (adjust as needed)
time.sleep(2)

# Navigate to the job search page
driver.get('https://www.glassdoor.com/Job/index.htm')

# Enter job title and location
searchbar_job = WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.ID, "searchBar-jobTitle")))
searchbar_job.clear()
searchbar_job.send_keys('data')

searchbar_location = WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.ID, "searchBar-location")))
searchbar_location.clear()
searchbar_location.send_keys('Morocco')
searchbar_location.send_keys(Keys.RETURN)

# Handle any pop-up dialog (if it appears)
try:
    skip_button = WebDriverWait(driver, 3).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, ".SVGInline.modal_closeIcon")))
    skip_button.click()
except Exception as e:
    print("Continue")

# Apply filters (Date posted and Company Size in this case)
date_posted = driver.find_element(
    By.XPATH, '//button[text()="Date posted"]')
date_posted.click()

duration_filter = driver.find_element(
    By.XPATH, "//div[contains(@class, 'SearchFiltersBar_dropdownOptionLabel__ZR1OK') and contains(text(), 'Last month')]")
duration_filter.click()

company_posted = driver.find_element(
    By.XPATH, '//*[@id="app-navigation"]/div[3]/div[1]/div[3]/div/button[2]')
company_posted.click()

company_filter = driver.find_element(
    By.XPATH, '//*[@id="app-navigation"]/div[3]/div[1]/div[3]/div[2]/ul/li[4]/button/div/div[6]')
company_filter.click()

# Continuously click on "Show More" until no more results are available
while True:
    try:
        show_more_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable(
            (By.CSS_SELECTOR, ".button_Button__meEg5.button-base_Button__9SPjH")))
        show_more_button.click()
        try:
            skip_button = WebDriverWait(driver, 3).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, ".SVGInline.modal_closeIcon")))
            skip_button.click()
        except Exception as e:
            print("Continue")
    except Exception as e:
        break

# Extract job listings
job_listings = driver.find_elements(
    By.CSS_SELECTOR, ".JobsList_jobListItem__JBBUV")

# Create a list to store the data
data = []

# Iterate through job listings and extract information
for job in job_listings:
    job_title = job.text.split('\n')[1]
    company = job.text.split('\n')[0]
    link = job.find_element(By.TAG_NAME, "a").get_attribute("href")
    region = job.text.split('\n')[-2]
    publish_duration = job.text.split('\n')[-1]

    data.append({
        "JobTitle": job_title,
        "Company": company,
        "Link": link,
        "Region": region,
        "PublishDuration": publish_duration
    })

# Quit the driver
driver.quit()

# Create a DataFrame from the extracted data
df = pd.DataFrame(data)

# Initialize a MongoDB client
mongo_client = pymongo.MongoClient("mongodb://your_mongodb_uri")

# Connect to the MongoDB database
db = mongo_client["your_database_name"]

# Define the collection where you want to insert the data
collection = db["your_collection_name"]

# Convert the data to a list of dictionaries
data_list = df.to_dict("records")

# Insert the data into the MongoDB collection
collection.insert_many(data_list)

# Close the MongoDB client connection
mongo_client.close()
