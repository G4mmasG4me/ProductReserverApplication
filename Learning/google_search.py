from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import os

driver = webdriver.Chrome(executable_path=os.getcwd() + r"\chromedriver.exe")
driver.set_window_position(0, 0)
driver.set_window_size(1900, 950)
driver.get("http://google.com")
driver.switch_to.frame(0)
continue_element = driver.find_element_by_id("introAgreeButton").submit()
search_bar = driver.find_element_by_name("q")
search_bar.send_keys("Hello How Are You Google?")
search_bar.submit()