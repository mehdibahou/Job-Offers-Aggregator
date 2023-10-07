import os
import time
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import pandas as pd
import boto3
import os
from io import StringIO


time.sleep(5)
options = webdriver.ChromeOptions()

options.add_argument("--headless")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")


driver = webdriver.Remote(
    command_executor='http://selenium:4444/wd/hub',
    options=options)
driver.get("https://www.linkedin.com/login/")
driver.maximize_window()
username = "snium008@gmail.com"
password = "Ma123456789@A"
username_field = driver.find_element(By.ID, "username")
print(username_field)
username_field.send_keys(username)
password_field = driver.find_element(By.ID, "password")
password_field.send_keys(password)
password_field.submit()
driver.get("https://www.linkedin.com/jobs/")
search_field = driver.find_element(
    By.CSS_SELECTOR, ".jobs-search-box__text-input.jobs-search-box__keyboard-text-input")
search_field.click()
search_field.send_keys("data")
time.sleep(3)
search_field.send_keys(Keys.RETURN)
time.sleep(3)
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
pagination = driver.find_element(
    By.XPATH, "/html/body/div[5]/div[3]/div[4]/div/div/main/div/div[1]/div/div[7]/ul")
pages = pagination.find_elements(By.TAG_NAME, "li")
time.sleep(3)
driver.execute_script("arguments[0].scrollIntoView(true);", pagination)
page = driver.find_element(
    By.XPATH, "/html/body/div[5]/div[3]/div[4]/div/div/main/div/div[1]/div/ul")
print(page)
time.sleep(3)
Data = []
stop = False
current_page = 0
while not stop:
    try:
        driver.execute_script(
            "arguments[0].scrollIntoView(true);", pagination)
        Jobtitles = driver.find_elements(
            By.CSS_SELECTOR, ".full-width.artdeco-entity-lockup__title.ember-view")
        Companies = driver.find_elements(
            By.CSS_SELECTOR, ".job-card-container__primary-description")
        Regions = driver.find_elements(
            By.CSS_SELECTOR, ".job-card-container__metadata-item")
        PublichDurations = driver.find_elements(By.TAG_NAME, "time")
        print(Jobtitles)
        print(
            "/#-----------------------------------------------------------------#/")
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
        time.sleep(3)
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
df = pd.DataFrame(Data)
driver.quit()
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
