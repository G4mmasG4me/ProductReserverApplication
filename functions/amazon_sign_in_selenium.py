from urllib.parse import urlparse

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.chrome.service import Service

from webdriver_manager.chrome import ChromeDriverManager
import time


import os

import wait_until_page_loaded

chrome_options = Options()
#chrome_options.add_argument("--headless")
#chrome_options.add_argument("--disable-extensions")
#chrome_options.add_argument("--disable-gpu")
chrome_options.add_experimental_option('detach', True)

s = Service(ChromeDriverManager().install())

driver = webdriver.Chrome(service=s, options=chrome_options)

amazon_sign_in_url_goto = '/gp/sign-in.html'
amazon_sign_in_url = '/ap/signin'
amazon_account_fix_up_url = '/ap/accountfixup'
amazon_password_reset_required = '/ap/forgotpassword/reverification'

sign_in_email = 'productreservertest@gmail.com'
sign_in_password = 'ProdReserve2022'

def sign_in_amazon():
  driver.get('https://www.amazon.co.uk' + amazon_sign_in_url_goto)
  if urlparse(driver.current_url).path == amazon_sign_in_url: # if currently on sign in page
    try: # try signing in
      email_input = driver.find_element(By.ID, 'ap_email')
      email_input.send_keys(sign_in_email)
      email_input.submit()
      if urlparse(driver.current_url).path == amazon_sign_in_url: # if currently on sign in page
        try: # tries to find if there is an error message, i.e. wrong email
          driver.find_element(By.ID, 'auth-error-message-box')
          return [False, 'Wrong Email']
        except NoSuchElementException as e: # if no error message box
          try: # tries to input password and submit
            password_input = driver.find_element(By.ID, 'ap_password')
            password_input.send_keys(sign_in_password)
            attempts = 0
            while sign_in_password != password_input.get_attribute('value') or attempts >= 5:
              attempts += 1
              password_input.clear()
              password_input.send_keys(sign_in_password)
            if sign_in_password == password_input.get_attribute('value'):
              password_input.submit()
            else:
              return [False, 'Failed Inputting Password Correctly']
              
            wait_until_page_loaded.wait_until_page_loaded(driver, 10) # waits until page loaded, checks 10 times, with 0.1 second between. max 1 second time to load
            # --- Redirected To Homepage | Logged In
            if urlparse(driver.current_url).path == '/':
              cookies = driver.get_cookies()
              return [True, cookies]
            
            # --- Phone Add Form --- #
            elif urlparse(driver.current_url).path == amazon_account_fix_up_url:
              try:
                add_phone_form = driver.find_element(By.ID, 'auth-account-fixup-phone-form')
                try:
                  skip_phone_button = driver.find_element(By.ID, 'ap-account-fixup-phone-skip-link')
                except NoSuchElementException as e:
                  return [False, 'Error Finding Skip Phone Button']
              except NoSuchElementException as e:
                return [False, 'Error Finding Add Phone Box']

            # --- Still On Login Page --- #
            elif urlparse(driver.current_url).path == amazon_sign_in_url: # tries to find if there is an error message, i.e. wrong password
              try:
                driver.find_element(By.ID, 'auth-warning-message-box')
                return [False, 'Wrong Password']
              except NoSuchElementException as e: # no error box
                return [False, 'Error Logging In: %s' % e]
            else:
              return [False, 'Unknown Destination']
          except NoSuchElementException as e: # if no password input box
            return [False, 'No Password Input'] 
          except Exception as e:
            return [False, 'Error Inputing Password: %s' % e]
        except Exception as e:
          return [False, 'Error Finding Error Box: %s' % e]
      else: # not on sign in page
        return [False, 'Not On Sign In Page']
    except NoSuchElementException as e: # if email input box not found
      return [False, 'No Email Input']
    except Exception as e:
      return [False, 'Error Inputing Email: %s' % e]
    finally:
      driver.quit()
  else:
    driver.quit()
    return [False, 'Not On Login Page']
    



output = sign_in_amazon()
print(output)

# cookies required to keep login
# ubid-acbuk
# x-acbuk
# session-token
# if you delete these cookies, then you get logged out