from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import os

driver = webdriver.Chrome(executable_path=os.getcwd() + r"\chromedriver.exe")
driver.get("https://www.amazon.co.uk/PlayStation-9395003-5-Console/dp/B08H95Y452")
price = driver.find_element_by_id("priceblock_ourprice")
print(price.text)