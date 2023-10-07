import os
import time
import pandas as pd
import pymongo
from io import StringIO
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

# Sleep for a few seconds to ensure the Selenium standalone server is ready
time.sleep(5)

# Set up Selenium ChromeOptions
options = webdriver.ChromeOptions()
options.add_argument("--headless")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")

# Initialize the WebDriver with the Selenium standalone server
driver = webdriver.Remote(
    command_executor='http://selenium:4444/wd/hub',
    options=options
)

# Navigate to LinkedIn and log in
driver.get("https://www.linkedin.com/login/")
driver.maximize_window()
username = "snium008@gmail.com"
password = "Ma123456789@A"
username_field = driver.find_element(By.ID, "username")
username_field.send_keys(username)
password_field = driver.find_element(By.ID, "password")
password_field.send_keys(password)
password_field.submit()

# Navigate to the LinkedIn jobs page
driver.get("https://www.linkedin.com/jobs/")
search_field = driver.find_element(
    By.CSS_SELECTOR, ".jobs-search-box__text-input.jobs-search-box__keyboard-text-input")
search_field.click()
search_field.send_keys("data")
time.sleep(3)
search_field.send_keys(Keys.RETURN)
time.sleep(3)

# Filter jobs by duration (e.g., "Last 30 days")
duration_field = driver.find_element(
    By.ID, "searchFilter_timePostedRange")
duration_field.click()
time.sleep(3)
duration_field = driver.find_element(
    By.XPATH, '/html/body/div[5]/div[3]/div[4]/section/div/section/div/div/div/ul/li[3]/div/div/div/div[1]/div/form/fieldset/div[1]/ul/li[2]/label/p')
duration_field.click()
time.sleep(3)
duration_field = driver.find_element(
    By.XPATH, "/html/body/div[5]/div[3]/div[4]/section/div/section/div/div/div/ul/li[3]/div/div/div/div[1]/div/form/fieldset/div[2]/button[2]")
duration_field.click()
time.sleep(3)

# Initialize data list
Data = []

# Define a flag to stop scraping when all pages are processed
stop = False
current_page = 0

# Scraping loop
while not stop:
    try:
        # Scroll to the bottom of the page to load more job listings
        driver.execute_script(
            "arguments[0].scrollIntoView(true);", pagination)

        # Extract job listings
        Jobtitles = driver.find_elements(
            By.CSS_SELECTOR, ".full-width.artdeco-entity-lockup__title.ember-view")
        Companies = driver.find_elements(
            By.CSS_SELECTOR, ".job-card-container__primary-description")
        Regions = driver.find_elements(
            By.CSS_SELECTOR, ".job-card-container__metadata-item")
        PublishDurations = driver.find_elements(By.TAG_NAME, "time")

        # Iterate through job listings and extract information
        for i in range(len(Jobtitles)):
            Jobtitles[i].click()
            time.sleep(1)
            full = driver.find_element(
                By.XPATH, '//*[@id="main"]/div/div[2]/div/div[2]/div[1]/div/div[1]/div/div[1]/div[1]/div[2]/div')
            date = full.find_elements(
                By.CSS_SELECTOR, ".tvm__text.tvm__text--neutral")
            mode = "On-site"
            try:
                mode = Regions[i].text.split("(")[1][:-1]
            except Exception as e:
                mode = "On-site"
            try:
                date = date[0].text
            except Exception as e:
                date = ""
            Data += [{
                "JobTitle": Jobtitles[i].text,
                "Company": Companies[i].text,
                "Link": Jobtitles[i].find_element(By.TAG_NAME, "a").get_attribute("href"),
                "Region": Regions[i].text,
                "Mode": mode,
                "PublishDuration": date,
            }]

        # Scroll to the next page or stop if all pages are processed
        pagination = driver.find_element(
            By.CSS_SELECTOR, ".artdeco-pagination__pages.artdeco-pagination__pages--number")
        pages = pagination.find_elements(By.TAG_NAME, "li")
        if current_page != 8:
            current_page = current_page + 1
            pages[current_page].click()
        else:
            pages[-4].click()
    except Exception as e:
        stop = True
        print(e)

# Create a DataFrame from the extracted data
df = pd.DataFrame(Data)

# Quit the driver
driver.quit()

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
