from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException
import os

chrome_options = Options()
#chrome_options.add_argument("--headless")
#chrome_options.add_argument("--disable-extensions")
#chrome_options.add_argument("--disable-gpu")

driver = webdriver.Chrome(executable_path=os.getcwd() + r"\chromedriver.exe", options=chrome_options)

amazon_basket_url = 'https://%s/gp/cart/view.html?ref_=nav_cart'
print(amazon_bakset_url)