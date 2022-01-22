from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException
import time
import os

chrome_options = Options()
#chrome_options.add_argument("--headless")
#chrome_options.add_argument("--disable-extensions")
#chrome_options.add_argument("--disable-gpu")

driver = webdriver.Chrome(executable_path=os.getcwd() + r"\chromedriver.exe", options=chrome_options)

ps4 = 'https://www.amazon.co.uk/dp/B01GVQVQH2/'
ps4_controller = 'https://www.amazon.co.uk/dp/B01GVQUX3U/'
amazon_sign_in_url = 'https://www.amazon.com/gp/sign-in.html'

def check_stock(url):
	driver.get(url)
	try:
		driver.find_element_by_id('priceblock_ourprice')
		return True
	except NoSuchElementException:
		return False

def buy_product(product_url):
	driver.get(product_url)
	WebDriverWait(driver, 4).until(ec.presence_of_element_located((By.ID, "sp-cc-accept"))).click()
	WebDriverWait(driver, 4).until(ec.presence_of_element_located((By.ID, "buy-now-button"))).click()
	# if we need to login, trigger sign in function

def add_to_basket(product_url):
	driver.get(product_url)
	driver.find_element_by_id('add-to-cart-button').click()

def buy_basket(product_url):
	driver.get()
	driver.find_element_by_id()

def sign_in(email, password):
	driver.get(amazon_sign_in_url)
	if driver.current_url.split('?')[0] == amazon_sign_in_url.split('?')[0]: # if currently on sign in page
		try:
			email_input = driver.find_element_by_id('ap_email')
			email_input.send_keys(email)
			email_input.submit()
			if driver.current_url.split('?')[0] == amazon_sign_in_url.split('?')[0]: # if currently on sign in page
				try: # tries to find if there is an error message, i.e. wrong email
					driver.find_element_by_id('auth-error-message-box')
					print('wrong email')
				except NoSuchElementException as e:
					try:
						password_input = driver.find_element_by_id('ap_password')
						password_input.send_keys(password)
						password_input.submit()
						try: # tries to find if there is an error message, i.e. wrong passwrod
							driver.find_element_by_id('auth-warning-message-box')
							print('wrong password')
						except NoSuchElementException as e:
							print('logged in')
					#except NoSuchElementException: as e:
		#else: # if not on sign in page
		print('not on sign in page')
		except NoSuchElementException as e:
			except NoSuchElementException as e: # if
	



#sign_in('domhough@hotmail.co.uk', 'test')
print(check_stock(ps4_controller))
time.sleep(100)