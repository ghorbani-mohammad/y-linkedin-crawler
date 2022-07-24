import pickle
import time
from django.conf import settings

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

def login():
    driver = webdriver.Remote("http://crawler_firefox:4444/wd/hub", DesiredCapabilities.FIREFOX)
    driver.get("https://www.linkedin.com/login")
    username_elem = driver.find_element("id", "username")
    username_elem.send_keys(settings.LINKEDIN_USERNAME)
    password_elem = driver.find_element("id", "password")
    password_elem.send_keys(settings.LINKEDIN_PASSWORD)
    password_elem.submit()
    WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.ID, "global-nav-search"))
    )
    pickle.dump(driver.get_cookies(), open("/app/crawler/cookies.pkl", "wb"))
    driver.quit()

def get_linkedin_feed():
    driver = webdriver.Remote("http://crawler_firefox:4444/wd/hub", DesiredCapabilities.FIREFOX)
    cookies = pickle.load(open("/app/crawler/cookies.pkl", "rb"))
    driver.get("https://www.linkedin.com/")
    for cookie in cookies:
        driver.add_cookie(cookie)
    driver.get("https://www.linkedin.com/feed/")
    WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.ID, "global-nav-search"))
    )
    articles = driver.find_elements(By.XPATH, ".//div[starts-with(@data-id, 'urn:li:activity:')]")
    for article in articles:
        driver.execute_script("arguments[0].scrollIntoView();", article)
        time.sleep(3)
        id = article.get_attribute("data-id")
        body = article.find_element(By.CLASS_NAME, "feed-shared-update-v2__commentary")
        print(id , body.text)
    driver.quit()
