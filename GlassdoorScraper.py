import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.microsoft import EdgeChromiumDriverManager


def GlassdoorScraper():
    driver = webdriver.Edge(EdgeChromiumDriverManager().install())
    driver.get("https://www.glassdoor.com/")
    driver.maximize_window()
    username = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, "input[name='username']")))
    username.clear()
    username.send_keys('XXXXXXXXXXXX')
    email_confirm = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, "button[type='submit']")))
    email_confirm.click()
    password = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, "input[name='password']")))
    password.clear()
    password.send_keys('XXXXXXXXXXXX')
    login = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, "button[type='submit']")))
    login.click()
    time.sleep(2)
    driver.get('https://www.glassdoor.com/Job/index.htm')
    searchbar_job = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.ID, "searchBar-jobTitle")))
    searchbar_job.clear()
    searchbar_job.send_keys('data')
    searchbar_location = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.ID, "searchBar-location")))
    searchbar_location.clear()
    searchbar_location.send_keys('Morocco')
    searchbar_location.send_keys(Keys.RETURN)
    try:
        skip_button = WebDriverWait(driver, 3).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, ".SVGInline.modal_closeIcon")))
        skip_button.click()
    except Exception as e:
        print("continue")
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
    still = True
    while still:
        try:
            Show_more = WebDriverWait(driver, 10).until(EC.element_to_be_clickable(
                (By.CSS_SELECTOR, ".button_Button__meEg5.button-base_Button__9SPjH")))
            Show_more.click()
            try:
                skip_button = WebDriverWait(driver, 3).until(
                    EC.element_to_be_clickable((By.CSS_SELECTOR, ".SVGInline.modal_closeIcon")))
                skip_button.click()
            except Exception as e:
                print("continue")
        except Exception as e:
            still = False
    All = driver.find_elements(By.CSS_SELECTOR, ".JobsList_jobListItem__JBBUV")
    Data = []
    for i in All:
        Data += [{
            "JobTitle": i.text.split('\n')[1],
            "Company": i.text.split('\n')[0],
            "Link":i.find_element(By.TAG_NAME, "a").get_attribute("href"),
            "Region": i.text.split('\n')[-2],
            "PublishDuration": i.text.split('\n')[-1],
        }]
    return Data
