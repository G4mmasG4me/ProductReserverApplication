from math import prod
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from urllib.parse import urlparse
import time

import amazon_sign_in_selenium

chrome_options = Options()
#chrome_options.add_argument("--headless")
#chrome_options.add_argument("--disable-extensions")
#chrome_options.add_argument("--disable-gpu")

s = Service(ChromeDriverManager().install())

amazon_basket_url = 'https://%s/gp/cart/view.html?ref_=nav_cart'
check_out_url_path = '/gp/buy/spc/handlers/display.html'
change_address_url = '/gp/buy/addressselect/handlers/display.html'


card_number = '1024204156346104'


def buy_amazon_product(prod_url, driver):
  parsed_prod_url = urlparse(prod_url)
  driver.get(prod_url)
  if driver.current_url == prod_url:
    try:
      cookies_accept_button = driver.find_element(By.ID, 'sp-cc-accept')
      cookies_accept_button.submit() # need to make sure that cookies accept button is in view, so scroll to that 
      try:
        buy_now_button = driver.find_element(By.ID, 'buy-now-button')
        buy_now_button.click()
        if urlparse(driver.current_url).path == check_out_url_path: # check if on checkout page
          # change delivery address
          try:
            change_address_button = driver.find_element(By.ID, 'addressChangeLinkId')
            change_address_button.click()
            if urlparse(driver.current_url).path == change_address_url:
              pass
            else:
              return [False, 'Not on Change Address URL']
          except NoSuchElementException:
            return [False, 'No Change Address Button']
          # check payment method
          # if payment method wrong change it 
          try:
            payment_last_4_digits = driver.find_element(By.XPATH, '//div[@data-field="tails"]')
            if payment_last_4_digits != card_number[-4:]:
              pass
            else:
              pass
              # change payment
          except NoSuchElementException:
            return [False, 'No Last 4 Digits of Payment Method']
        elif driver.current_url == prod_url: # if still on product page
          try: # check for checkout popout checkout
            pass
          except NoSuchElementException: # no popout checkout, so fail
            print('No Checkout Box')

          except Exception as e: # 
            print('Failed To Find Checkout')
            print('Error: %s' % e)
      except Exception as e:
        print('Failed Adding To Cart')
        print('Error: %s' % e)

    except NoSuchElementException:
      print('No Cookies Button')
    except Exception as e:
      print('Failed To Click Accept Cookie Button')
      print('Error: %s' % e)

    

prod_url = 'https://www.amazon.co.uk/dp/B009DL2TBA'
order_details = []
amazon_signed_in, amazon_sign_in_cookies = amazon_sign_in_selenium.sign_in_amazon()
if amazon_signed_in is True:
  parsed_prod_url = urlparse(prod_url)
  tld = parsed_prod_url.netloc.split('.')[-1]

  # edits cookie names depending on their amazon region using TLDs
  if parsed_prod_url.netloc != 'www.amazon.com':
    amazon_sign_in_cookies[0]['name'] = 'ubid-acb' + str(tld)
    amazon_sign_in_cookies[1]['name'] = 'x-acb' + str(tld)

  driver = webdriver.Chrome(service=s, options=chrome_options)
  
  driver.execute_cdp_cmd('Network.enable', {})

  for cookie in amazon_sign_in_cookies:
    cookie['domain'] = str(parsed_prod_url.netloc)
    driver.execute_cdp_cmd('Network.setCookie', cookie)

  driver.execute_cdp_cmd('Network.disable', {})
  
  buy_amazon_product(prod_url, driver)
