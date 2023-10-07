import os
import time
import pandas as pd
import boto3
from io import StringIO
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys


time.sleep(5)
options = webdriver.ChromeOptions()

options.add_argument("--headless")

driver = webdriver.Remote(
    command_executor='http://selenium:4444/wd/hub',
    options=options)
driver.get("https://ma.indeed.com/jobs?q=data&fromage=14")
driver.maximize_window()
job_number = driver.find_element(
    By.CSS_SELECTOR, ".jobsearch-JobCountAndSortPane-jobCount.css-1af0d6o.eu4oa1w0")
Data = []
for i in range(int(job_number.text.split(" ")[0]) // 15):
    if i != 0:
        driver.get(
            "https://ma.indeed.com/jobs?q=data&fromage=14&start="+str(i*10))
    time.sleep(2)
    All = driver.find_elements(By.CSS_SELECTOR, ".css-5lfssm.eu4oa1w0")
    for i in All:
        if len(i.text.split('\n')) > 1:
            Data += [{
                "JobTitle": i.text.split('\n')[0],
                "Company": i.text.split('\n')[1],
                "Link":i.find_element(By.TAG_NAME, "a").get_attribute("href"),
                "Region": i.text.split('\n')[2],
                "PublishDuration": i.text.split('\n')[-1],
            }]
driver.quit()
df = pd.DataFrame(Data)
AWS_ACCESS_KEY_ID = 'AKIAYBL4RI3YLV4UXCHM'
AWS_SECRET_ACCESS_KEY = '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'

s3 = boto3.client('s3',
                  aws_access_key_id=AWS_ACCESS_KEY_ID,
                  aws_secret_access_key=AWS_SECRET_ACCESS_KEY)

bucket_name = 'map-opp-data'
csv_buffer = StringIO()
df.to_csv(csv_buffer, index=False)
object_key = 'data.csv'
s3.put_object(Bucket=bucket_name, Key=object_key, Body=csv_buffer.getvalue())
