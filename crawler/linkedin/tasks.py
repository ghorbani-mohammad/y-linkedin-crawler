import pickle
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

