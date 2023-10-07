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

# Initialize the WebDriver with the Selenium standalone server
driver = webdriver.Remote(
    command_executor='http://selenium:4444/wd/hub',
    options=options
)

# Navigate to the Indeed job search page
driver.get("https://ma.indeed.com/jobs?q=data&fromage=14")
driver.maximize_window()

# Get the total number of job listings
job_number = driver.find_element(
    By.CSS_SELECTOR, ".jobsearch-JobCountAndSortPane-jobCount.css-1af0d6o.eu4oa1w0")

# Create a list to store the scraped data
Data = []

# Loop through the job listings
for i in range(int(job_number.text.split(" ")[0]) // 15):
    if i != 0:
        driver.get(
            "https://ma.indeed.com/jobs?q=data&fromage=14&start="+str(i*10))
    time.sleep(2)
    All = driver.find_elements(By.CSS_SELECTOR, ".css-5lfssm.eu4oa1w0")
    for i in All:
        if len(i.text.split('\n')) > 1:
            Data.append({
                "JobTitle": i.text.split('\n')[0],
                "Company": i.text.split('\n')[1],
                "Link": i.find_element(By.TAG_NAME, "a").get_attribute("href"),
                "Region": i.text.split('\n')[2],
                "PublishDuration": i.text.split('\n')[-1],
            })

# Quit the driver
driver.quit()

# Create a DataFrame from the extracted data
df = pd.DataFrame(Data)

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
