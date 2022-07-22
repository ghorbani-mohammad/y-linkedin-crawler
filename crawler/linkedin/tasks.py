from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

def login():
    driver = webdriver.Remote("http://crawler_firefox:4444/wd/hub", DesiredCapabilities.FIREFOX)
    driver.get("https://www.linkedin.com/login")