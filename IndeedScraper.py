
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from webdriver_manager.microsoft import EdgeChromiumDriverManager


def IndeedScraper():

    driver = webdriver.Edge(EdgeChromiumDriverManager().install())
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
    return Data
